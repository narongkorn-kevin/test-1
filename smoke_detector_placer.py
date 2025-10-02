#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke Detector Auto-Placer for DXF
- Easy to use: Just provide input DXF file
- Automatically places smoke detectors according to international standards
- Exports DXF with detectors and PDF preview
"""

import argparse
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import ezdxf
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
try:
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    HAS_DRAWING = True
except ImportError:
    HAS_DRAWING = False
    print("Warning: ezdxf drawing add-on not available")


def parse_args():
    p = argparse.ArgumentParser(
        description="Auto-place smoke detectors in rooms from a DXF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Simple usage (automatic detection):
    python smoke_detector_placer.py input.dxf
  
  Custom output names:
    python smoke_detector_placer.py input.dxf --out output.dxf --pdf preview.pdf
  
  Specify room layer:
    python smoke_detector_placer.py input.dxf --rooms-layer ROOMS,WALLS
  
  Use EN54-14 standard:
    python smoke_detector_placer.py input.dxf --std EN54-14
        """
    )
    p.add_argument("in_path", help="Input DXF file path")
    p.add_argument("--out", dest="out_path", default=None, 
                   help="Output DXF path (default: input_with_detectors.dxf)")
    p.add_argument("--pdf", dest="pdf_path", default=None,
                   help="Output PDF preview path (default: input_preview.pdf)")
    p.add_argument("--csv", dest="csv_path", default=None, help="Optional CSV export path")
    p.add_argument("--rooms-layer", dest="room_layers", default=None,
                   help="Comma-separated layer names containing rooms (default: auto-detect)")
    p.add_argument("--std", dest="standard", choices=["NFPA72", "EN54-14", "CUSTOM"], default="NFPA72",
                   help="Spacing standard (default: NFPA72)")
    p.add_argument("--spacing", dest="spacing", type=float, default=None,
                   help="Custom spacing in meters between detectors")
    p.add_argument("--margin", dest="margin", type=float, default=0.5,
                   help="Wall clearance margin in meters (default: 0.5)")
    p.add_argument("--grid", dest="grid", choices=["square", "hex"], default="square",
                   help="Grid style: square or hex (default: square)")
    p.add_argument("--min-room-area", dest="min_area", type=float, default=1.0,
                   help="Skip rooms smaller than this area in m² (default: 1.0)")
    p.add_argument("--units", dest="units", choices=["m", "mm", "ft", "in"], default=None,
                   help="Drawing units (default: auto-detect)")
    p.add_argument("--room-name-layer", dest="room_name_layer", default=None,
                   help="Layer containing room name text")
    p.add_argument("--inspect", action="store_true", 
                   help="Inspect DXF layers and polygons, then exit")
    p.add_argument("--no-pdf", action="store_true",
                   help="Skip PDF generation")
    p.add_argument("--offset-x", dest="offset_x", type=float, default=None,
                   help="X offset to shift detector positions (auto-detect if not specified)")
    p.add_argument("--offset-y", dest="offset_y", type=float, default=None,
                   help="Y offset to shift detector positions")
    return p.parse_args()


def auto_detect_units(doc) -> str:
    """Auto-detect the units used in the DXF file based on drawing size."""
    msp = doc.modelspace()
    try:
        box = msp.bbox()
        max_dim = max(box.size.x, box.size.y)
    except Exception:
        minx, miny, maxx, maxy = _bbox_fallback(msp)
        max_dim = max(maxx - minx, maxy - miny)
    
    if max_dim > 2000:
        return "mm"
    elif max_dim > 50:
        return "m"
    else:
        return "m"


def auto_detect_room_layers(doc) -> List[str]:
    """Auto-detect layers that contain closed polygons (likely rooms)."""
    from collections import defaultdict
    msp = doc.modelspace()
    counts = defaultdict(int)
    
    for e in msp.query("LWPOLYLINE"):
        try:
            if e.closed:
                pts = [(v[0], v[1]) for v in e.get_points()]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    counts[e.dxf.layer.upper()] += 1
        except Exception:
            pass
    
    for e in msp.query("POLYLINE"):
        try:
            if e.is_closed:
                pts = [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    counts[e.dxf.layer.upper()] += 1
        except Exception:
            pass
    
    # Return layers with at least 1 closed polygon
    detected = [layer for layer, count in counts.items() if count >= 1]
    return detected if detected else ["ROOMS"]


def auto_detect_offset(doc, rooms: List[Tuple[str, Polygon]], room_layers: List[str]) -> Tuple[float, float]:
    """Auto-detect offset to align rooms with main architectural drawing."""
    if not rooms:
        return 0.0, 0.0
    
    msp = doc.modelspace()
    
    # Get room bounds
    room_xs = []
    room_ys = []
    for _, poly in rooms:
        bounds = poly.bounds
        room_xs.extend([bounds[0], bounds[2]])
        room_ys.extend([bounds[1], bounds[3]])
    
    room_minx, room_maxx = min(room_xs), max(room_xs)
    room_miny, room_maxy = min(room_ys), max(room_ys)
    room_centerx = (room_minx + room_maxx) / 2
    room_centery = (room_miny + room_maxy) / 2
    
    # Priority list: architectural layers that typically define the building
    priority_keywords = ["WALL", "A-WALL", "I-WALL", "ARCH", "A-CLNG", "A-DOOR", "A-WIND"]
    
    # Convert room_layers to set for faster lookup
    room_layer_set = set(room_layers)
    
    # First, try to find architectural layers
    from collections import defaultdict
    layer_coords = defaultdict(lambda: {"xs": [], "ys": [], "count": 0})
    
    for e in msp:
        try:
            layer = e.dxf.layer.upper()
            # Skip room layers
            if layer in room_layer_set:
                continue
            
            dxftype = e.dxftype()
            
            if dxftype == "LINE":
                layer_coords[layer]["xs"].extend([e.dxf.start.x, e.dxf.end.x])
                layer_coords[layer]["ys"].extend([e.dxf.start.y, e.dxf.end.y])
                layer_coords[layer]["count"] += 1
            elif dxftype == "LWPOLYLINE":
                for v in e.get_points():
                    layer_coords[layer]["xs"].append(v[0])
                    layer_coords[layer]["ys"].append(v[1])
                layer_coords[layer]["count"] += 1
        except Exception:
            pass
    
    # Find the best architectural layer
    priority_xs = []
    priority_ys = []
    priority_layer_found = None
    
    # Try priority keywords first
    for keyword in priority_keywords:
        for layer, data in layer_coords.items():
            if keyword in layer and data["count"] > 10:  # Must have reasonable number of entities
                priority_xs.extend(data["xs"])
                priority_ys.extend(data["ys"])
                if not priority_layer_found:
                    priority_layer_found = layer
    
    # If no priority layers found, use the layer with most entities
    if not priority_xs:
        sorted_layers = sorted(layer_coords.items(), key=lambda x: -x[1]["count"])
        if sorted_layers:
            for layer, data in sorted_layers[:3]:  # Use top 3 layers
                priority_xs.extend(data["xs"])
                priority_ys.extend(data["ys"])
                if not priority_layer_found:
                    priority_layer_found = layer
    
    if not priority_xs:
        print("⚠️  Could not auto-detect offset (no suitable layers found)")
        return 0.0, 0.0
    
    main_minx, main_maxx = min(priority_xs), max(priority_xs)
    main_miny, main_maxy = min(priority_ys), max(priority_ys)
    main_centerx = (main_minx + main_maxx) / 2
    main_centery = (main_miny + main_maxy) / 2
    
    # Calculate offset to align centers
    offset_x = main_centerx - room_centerx
    offset_y = main_centery - room_centery
    
    # Check if offset is significant (> 1% of drawing size)
    room_size = max(room_maxx - room_minx, room_maxy - room_miny)
    offset_magnitude = (offset_x**2 + offset_y**2)**0.5
    
    if offset_magnitude < room_size * 0.01:
        # Offset is negligible, rooms are likely already aligned
        print(f"✅ Rooms are already aligned with main drawing (offset < 1%)")
        return 0.0, 0.0
    
    print(f"")
    print(f"🔍 Auto-detected drawing offset:")
    print(f"   Rooms center: ({room_centerx:.0f}, {room_centery:.0f})")
    print(f"   Main drawing center: ({main_centerx:.0f}, {main_centery:.0f})")
    if priority_layer_found:
        print(f"   Reference layer: {priority_layer_found}")
    print(f"   Applying offset: ({offset_x:.0f}, {offset_y:.0f})")
    
    return offset_x, offset_y


def unit_scale(units: str) -> float:
    if units == "m":
        return 1.0
    if units == "mm":
        return 1000.0
    if units == "ft":
        return 1.0 / 0.3048
    if units == "in":
        return 1.0 / 0.0254
    return 1.0


def dxf_to_room_polygons(doc, layers: List[str]) -> List[Tuple[str, Polygon]]:
    msp = doc.modelspace()
    polys: List[Tuple[str, Polygon]] = []

    def lwpoly_to_poly(e):
        pts = [(v[0], v[1]) for v in e.get_points()]
        if pts and pts[0] != pts[-1]:
            pts.append(pts[0])
        return Polygon(pts)

    for e in msp.query("LWPOLYLINE"):
        try:
            if e.dxf.layer.upper() in layers and e.closed:
                poly = lwpoly_to_poly(e)
                if poly.is_valid and poly.area > 0:
                    polys.append((e.dxf.layer, poly))
        except Exception:
            continue

    for e in msp.query("POLYLINE"):
        try:
            if e.dxf.layer.upper() in layers and e.is_closed:
                pts = [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    polys.append((e.dxf.layer, poly))
        except Exception:
            continue

    return polys


def map_room_names(doc, polygons: List[Polygon], name_layer: str) -> Dict[int, str]:
    msp = doc.modelspace()
    texts = []
    for e in msp.query("TEXT MTEXT"):
        try:
            if e.dxf.layer.upper() == name_layer:
                # TEXT vs MTEXT text extraction
                try:
                    txt = e.dxf.text if e.dxftype() == "TEXT" else e.text
                except Exception:
                    try:
                        txt = e.plain_text()
                    except Exception:
                        txt = ""
                if not txt:
                    continue
                # insertion point
                try:
                    x = float(e.dxf.insert.x)
                    y = float(e.dxf.insert.y)
                except Exception:
                    try:
                        x = float(e.dxf.location.x)
                        y = float(e.dxf.location.y)
                    except Exception:
                        continue
                texts.append((txt.strip(), (x, y)))
        except Exception:
            continue

    names: Dict[int, str] = {}
    centroids = [p.centroid for p in polygons]
    for i, c in enumerate(centroids):
        if not texts:
            break
        cx, cy = c.x, c.y
        nearest = min(texts, key=lambda t: (t[1][0] - cx) ** 2 + (t[1][1] - cy) ** 2)
        names[i] = nearest[0]
    return names


def hex_grid_points_in_poly(poly: Polygon, spacing: float):
    minx, miny, maxx, maxy = poly.bounds
    h = spacing * math.sin(math.radians(60))
    points = []
    y = miny
    row = 0
    while y <= maxy:
        offset = 0.0 if row % 2 == 0 else spacing * 0.5
        x = minx + offset
        while x <= maxx:
            pt = Point(x, y)
            if poly.contains(pt):
                points.append((x, y))
            x += spacing
        y += h
        row += 1
    return points


def square_grid_points_in_poly(poly: Polygon, spacing: float):
    minx, miny, maxx, maxy = poly.bounds
    xs = np.arange(minx, maxx + spacing * 0.5, spacing)
    ys = np.arange(miny, maxy + spacing * 0.5, spacing)
    pts = []
    for y in ys:
        for x in xs:
            if poly.contains(Point(x, y)):
                pts.append((x, y))
    return pts


def compute_spacing(standard: str, custom_spacing: float | None):
    if custom_spacing and custom_spacing > 0:
        return float(custom_spacing), "CUSTOM spacing provided by user."
    if standard == "NFPA72":
        return 9.1, "NFPA 72 smooth-ceiling nominal spacing (~30 ft)."
    if standard == "EN54-14":
        return 8.66, "EN 54-14 style conservative spacing targeting ≤7.5 m to nearest detector (hex grid recommended)."
    return 9.1, "Default spacing used (NFPA-like)."


def offset_interior(poly: Polygon, margin: float) -> Polygon:
    inset = poly.buffer(-margin, join_style=2)
    if inset.is_empty:
        return poly
    if inset.geom_type == "MultiPolygon":
        areas = [(g.area, g) for g in inset.geoms]
        return max(areas, key=lambda t: t[0])[1]
    return inset


def place_detectors_in_room(room_poly: Polygon, spacing_units: float, margin_units: float, grid_type: str):
    if room_poly.area <= 0:
        return []
    inner = offset_interior(room_poly, margin_units)
    if inner.is_empty:
        return []
    if grid_type == "hex":
        pts = hex_grid_points_in_poly(inner, spacing_units)
    else:
        pts = square_grid_points_in_poly(inner, spacing_units)
    if not pts:
        c = inner.centroid
        if inner.contains(c):
            pts = [(c.x, c.y)]
    return pts


def write_output_dxf(src_doc, out_path: Path, points_by_room: List[Dict], offset_x: float = 0.0, offset_y: float = 0.0):
    doc = src_doc
    msp = doc.modelspace()

    # Calculate appropriate symbol size based on drawing extents
    try:
        bbox = msp.bbox()
        max_dim = max(bbox.size.x, bbox.size.y)
    except Exception:
        # Fallback to calculating from entities
        minx, miny, maxx, maxy = _bbox_fallback(msp)
        max_dim = max(maxx - minx, maxy - miny)
    
    # Symbol size: about 0.3-0.5% of drawing dimension (visible but not overwhelming)
    symbol_radius = max_dim * 0.004  # 0.4%
    cross_size = symbol_radius * 1.5

    layer_name = "SMOKE_DETECTORS"
    try:
        if layer_name not in doc.layers:
            doc.layers.add(name=layer_name, color=1)  # Red color
    except Exception:
        try:
            doc.layers.add(layer_name)
        except Exception:
            pass

    blk_name = "SMOKE_DET_SYMBOL"
    if blk_name not in doc.blocks:
        blk = doc.blocks.new(name=blk_name)
        # Circle for detector
        blk.add_circle(center=(0, 0), radius=symbol_radius, dxfattribs={"color": 1})
        # Crosshair
        blk.add_line((-cross_size, 0), (cross_size, 0), dxfattribs={"color": 1})
        blk.add_line((0, -cross_size), (0, cross_size), dxfattribs={"color": 1})

    total_placed = 0
    for room in points_by_room:
        for (x, y) in room["points"]:
            # Apply offset to align with main drawing
            adjusted_x = x + offset_x
            adjusted_y = y + offset_y
            msp.add_blockref(blk_name, insert=(adjusted_x, adjusted_y), dxfattribs={"layer": layer_name})
            total_placed += 1

    doc.saveas(out_path.as_posix())
    
    return total_placed


def write_csv(csv_path: Path, points_by_room: List[Dict]):
    import csv
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["room_index", "room_name", "x", "y"])
        for room in points_by_room:
            idx = room["index"]
            name = room.get("name", "")
            for (x, y) in room["points"]:
                w.writerow([idx, name, f"{x:.3f}", f"{y:.3f}"])


def generate_pdf_preview_simple(pdf_path: Path, dxf_with_detectors_path: Path):
    """Generate a simple PDF preview (smoke detectors only for large files)."""
    
    print("💡 Note: For best quality, open the DXF file directly in AutoCAD/DWG viewer")
    print("   and print to PDF. This gives you full quality with all details.")
    print("")
    print(f"   The DXF file with detectors: {dxf_with_detectors_path}")
    
    # Skip PDF generation for now as it's too slow for large files
    # User should use their CAD software to export to PDF
    return


def _bbox_fallback(msp):
    minx = miny = float("inf")
    maxx = maxy = float("-inf")
    def upd(x, y):
        nonlocal minx, miny, maxx, maxy
        minx = min(minx, x); miny = min(miny, y)
        maxx = max(maxx, x); maxy = max(maxy, y)
    try:
        for e in msp:
            dxftype = e.dxftype()
            if dxftype in ("LINE", "LWPOLYLINE", "POLYLINE", "CIRCLE", "ARC", "SPLINE", "ELLIPSE", "POINT"):
                try:
                    box = e.bbox()
                    if box is None:
                        continue
                    (x1, y1, _), (x2, y2, _) = box.extmin, box.extmax
                    upd(x1, y1); upd(x2, y2)
                except Exception:
                    if dxftype in ("LWPOLYLINE", "POLYLINE"):
                        try:
                            if dxftype == "LWPOLYLINE":
                                pts = [(v[0], v[1]) for v in e.get_points()]
                            else:
                                pts = [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
                            for x, y in pts:
                                upd(x, y)
                        except Exception:
                            pass
    except Exception:
        pass
    if minx == float("inf"):
        return 0.0, 0.0, 0.0, 0.0
    return minx, miny, maxx, maxy


def inspect_dxf(doc):
    msp = doc.modelspace()
    from collections import defaultdict
    counts = defaultdict(int)
    areas = defaultdict(float)

    for e in msp.query("LWPOLYLINE"):
        try:
            if e.closed:
                pts = [(v[0], v[1]) for v in e.get_points()]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    counts[e.dxf.layer] += 1
                    areas[e.dxf.layer] += poly.area
        except Exception:
            pass

    for e in msp.query("POLYLINE"):
        try:
            if e.is_closed:
                pts = [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
                if pts and pts[0] != pts[-1]:
                    pts.append(pts[0])
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    counts[e.dxf.layer] += 1
                    areas[e.dxf.layer] += poly.area
        except Exception:
            pass

    try:
        box = msp.bbox()
        w = box.size.x
        h = box.size.y
        max_dim = max(w, h)
    except Exception:
        minx, miny, maxx, maxy = _bbox_fallback(msp)
        w = maxx - minx
        h = maxy - miny
        max_dim = max(w, h)

    if max_dim > 2000:
        units_guess = "mm"
    elif max_dim > 50:
        units_guess = "m"
    else:
        units_guess = "m"

    print("=== INSPECT REPORT ===")
    print(f"Approx drawing size (units): W={w:.2f}, H={h:.2f}, max={max_dim:.2f}")
    print(f"Units guess: {units_guess}")
    print(f"Closed polygons by layer:")
    for layer, cnt in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  - {layer}: {cnt} closed polys, total area={areas[layer]:.2f}")
    print("======================")


def main():
    args = parse_args()
    in_path = Path(args.in_path)
    
    # Auto-generate output paths if not specified
    if args.out_path is None:
        out_path = in_path.parent / f"{in_path.stem}_with_detectors.dxf"
    else:
        out_path = Path(args.out_path)
    
    if args.pdf_path is None and not args.no_pdf:
        pdf_path = in_path.parent / f"{in_path.stem}_preview.pdf"
    else:
        pdf_path = Path(args.pdf_path) if args.pdf_path else None
    
    csv_path = Path(args.csv_path) if args.csv_path else None

    if not in_path.exists():
        print(f"❌ Input DXF not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("🔥 Smoke Detector Auto-Placer")
    print("=" * 60)
    print(f"📁 Reading: {in_path}")
    
    try:
        doc = ezdxf.readfile(in_path.as_posix())
    except Exception as e:
        print(f"❌ Failed to read DXF: {e}", file=sys.stderr)
        sys.exit(1)

    if args.inspect:
        try:
            inspect_dxf(doc)
        except Exception as e:
            print(f"❌ Inspect failed: {e}", file=sys.stderr)
        sys.exit(0)

    # Auto-detect units if not specified
    if args.units is None:
        detected_units = auto_detect_units(doc)
        print(f"🔍 Auto-detected units: {detected_units}")
        units = detected_units
    else:
        units = args.units
        print(f"📏 Using specified units: {units}")
    
    # Auto-detect room layers if not specified
    if args.room_layers is None:
        detected_layers = auto_detect_room_layers(doc)
        print(f"🔍 Auto-detected room layers: {', '.join(detected_layers)}")
        room_layers = detected_layers
    else:
        room_layers = [s.strip().upper() for s in args.room_layers.split(",") if s.strip()]
        print(f"📋 Using specified layers: {', '.join(room_layers)}")
    
    spacing_m, spacing_note = compute_spacing(args.standard, args.spacing)
    print(f"📐 {spacing_note}")
    print(f"⚙️  Standard: {args.standard}, Grid: {args.grid}")

    scale = unit_scale(units)
    spacing_units = spacing_m * scale
    margin_units = args.margin * scale

    rooms = dxf_to_room_polygons(doc, room_layers)
    if not rooms:
        print("❌ No closed room polygons found on specified layers.", file=sys.stderr)
        print("💡 Try running with --inspect to see available layers.")
        sys.exit(1)

    names_map: Dict[int, str] = {}
    if args.room_name_layer:
        names_map = map_room_names(doc, [p for _, p in rooms], args.room_name_layer.upper())

    print(f"🏠 Found {len(rooms)} rooms")
    
    # Auto-detect or use specified offset
    if args.offset_x is not None and args.offset_y is not None:
        offset_x = args.offset_x
        offset_y = args.offset_y
        print(f"📍 Using specified offset: ({offset_x:.0f}, {offset_y:.0f})")
    else:
        offset_x, offset_y = auto_detect_offset(doc, rooms, room_layers)
    
    points_by_room: List[Dict] = []
    for i, (layer, poly) in enumerate(rooms):
        area_m2 = poly.area / (scale ** 2)
        if area_m2 < args.min_area:
            continue
        pts = place_detectors_in_room(poly, spacing_units, margin_units, args.grid)
        points_by_room.append({
            "index": i,
            "layer": layer,
            "name": names_map.get(i, ""),
            "points": pts,
        })

    total = sum(len(r["points"]) for r in points_by_room)
    
    # Write output DXF with offset
    print(f"💾 Saving DXF with detectors: {out_path}")
    total_placed = write_output_dxf(doc, out_path, points_by_room, offset_x, offset_y)
    
    if total_placed != total:
        print(f"⚠️  Warning: Expected {total} but placed {total_placed} detectors")
    
    # Write CSV if requested
    if csv_path:
        print(f"📊 Saving CSV: {csv_path}")
        write_csv(csv_path, points_by_room)
    
    # Note about PDF generation
    if pdf_path and not args.no_pdf:
        print("")
        print("=" * 60)
        generate_pdf_preview_simple(pdf_path, out_path)
        print("=" * 60)

    print("=" * 60)
    print("✅ COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   • Rooms found: {len(rooms)}")
    print(f"   • Rooms processed (≥ {args.min_area} m²): {len(points_by_room)}")
    print(f"   • Total detectors placed: {total}")
    print(f"   • Average detectors per room: {total/len(points_by_room):.1f}" if points_by_room else "")
    print("=" * 60)


if __name__ == "__main__":
    main()
