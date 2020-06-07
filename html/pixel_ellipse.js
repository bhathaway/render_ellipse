// I want this python script to be able to generate ascii art
// of ellipses based on command line parameters.

import {ConvexPolygon} from './convex_polygon.js'

class Pixel
{
    constructor(x, y)
    {
        this.x = x;
        this.y = y;
        let v = [[x, y], [x+1., y], [x+1., y+1.], [x, y+1.]];
        this.poly = new ConvexPolygon(v);
    }

    trim_outer(p0, p1, reverse = false)
    {
        console.assert((typeof p0 == 'object') && (Array.isArray(p0)),
          'p0 must be an array');
        console.assert(p0.length >= 2, 'Not enough coordinates in p0');
        console.assert((typeof p1 == 'object') && (Array.isArray(p1)),
          'p1 must be an array');
        console.assert(p1.length >= 2, 'Not enough coordinates in p1');
        let tri = new ConvexPolygon([[0., 0.], p0, p1]);
        // We are assuming that the origin is interior to the ellipse,
        // so that we can use the sign of the counterclockwise area
        // equation to determine the vertex order.
        // Ignore double solutions. We can only get away with
        // this because we're using unit thickness ellipses.
        let eps = 0.00001
        let a = tri.area()

        let swap = false;
        if (Math.abs(a) < eps) {
            return;
        } else if (reverse) {
            if (a > 0) {
                swap = true;
            }
        } else {
            if (a < 0) {
                swap = true;
            }
        }

        if (swap) {
            let temp = p1;
            p1 = p0;
            p0 = temp;
        }

        this.poly.trim(p0, p1);
    }

    // Inner ellipse vertex ordering is clockwise.
    trim_inner(p0, p1)
    {
        this.trim_outer(p0, p1, true);
    }
}

class Ellipse
{
    constructor(a, b, th, nudge = [0., 0.])
    {
        this.a = Number(a);
        this.b = Number(b);
        this.th = Number(th);
        this.nudge = nudge;
        let c = Math.cos(th);
        let s = Math.sin(th);
        this.A = (c*c)/(a*a) + (s*s)/(b*b);
        this.B = 2*c*s*(1.0/(a*a) - 1.0/(b*b));
        this.C = (s*s)/(a*a) + (c*c)/(b*b);
    }

    solve_y(x)
    {
        let A = this.A;
        let B = this.B;
        let C = this.C;
        let x0 = this.nudge[0];
        let y0 = this.nudge[1];
        let u = x - x0;
        let det = -4*A*C*u*u + B*B*u*u + 4*C;
        if (det >= 0) {
            let r = Math.sqrt(det);
            return [(r-B*u)/(2*C)+y0, (-r-B*u)/(2*C)+y0];
        } else {
            return null;
        }
    }

    solve_x(y)
    {
        let A = this.A;
        let B = this.B;
        let C = this.C;
        let x0 = this.nudge[0];
        let y0 = this.nudge[1];
        let v = y - y0;
        let det = -4*A*C*v*v + B*B*v*v + 4*A;
        if (det >= 0) {
            let r = Math.sqrt(det);
            return [(r-B*v)/(2*A)+x0, (-r-B*v)/(2*A)+x0];
        } else {
            return null;
        }
    }
}

function ellipse_points(e)
{
    console.assert((typeof e == 'object') && (e instanceof Ellipse),
      'Wrong type for e');
    let p = [];
    let x = 0.;
    let seeking = true;
    while (seeking) {
        let y_pair = e.solve_y(x);
        if (y_pair) {
            p.push([x, y_pair[0]]);
            p.push([x, y_pair[1]]);
        } else {
            seeking = false;
        }
        x += 1.;
    }

    seeking = true;
    x = -1.;
    while (seeking) {
        let y_pair = e.solve_y(x);
        if (y_pair) {
            p.push([x, y_pair[0]]);
            p.push([x, y_pair[1]]);
        } else {
            seeking = false;
        }
        x -= 1.;
    }

    seeking = true;
    let y = 0.;
    while (seeking) {
        let x_pair = e.solve_x(y);
        if (x_pair) {
            p.push([x_pair[0], y]);
            p.push([x_pair[1], y]);
        } else {
            seeking = false;
        }
        y += 1.;
    }

    seeking = true;
    y = -1.;
    while (seeking) {
        let x_pair = e.solve_x(y);
        if (x_pair) {
            p.push([x_pair[0], y]);
            p.push([x_pair[1], y]);
        } else {
            seeking = false;
        }
        y -= 1.;
    }

    return p;
}

function raster_ellipse(a, b, th, nudge)
{
    console.assert(a > 1. && b > 1., "a and b should be greater than 1");
    let min_x = null;
    let max_x = null;
    let min_y = null;
    let max_y = null;
    let eps = 0.00001;
    let outer = new Ellipse(a, b, th, nudge);
    let inner = new Ellipse(a-1., b-1., th, nudge);
    
    let outer_points = ellipse_points(outer);
    let inner_points = ellipse_points(inner);
    let both = inner_points.concat(outer_points);

    // Now create a sparse array of pixels from the lists.
    // For now I'm going to re-solve. I know it's inefficient, so
    // that will be something to optimize.
    let candidates = new Set();
    for (let point of both) {
        let x = point[0];
        let y = point[1];
        candidates.add([Math.floor(x), Math.floor(y)]);
        if (Math.floor(x) == x) {
            // Include both sides
            candidates.add([Math.floor(x)-1, Math.floor(y)]);
        }
        if (Math.floor(y) == y) {
            candidates.add([Math.floor(x), Math.floor(y)-1]);
        }
    }

    let pixels = {};
    for (let c of candidates) {
        let x = c[0];
        let y = c[1];
        if (!min_x) {
            min_x = x;
            max_x = x;
            min_y = y;
            max_y = y;
        }
        if (x > max_x) {
            max_x = x;
        }
        if (x < min_x) {
            min_x = x;
        }
        if (y > max_y) {
            max_y = y;
        }
        if (y < min_y) {
            min_y = y;
        }

        if (! ([x, y] in pixels)) {
            let p = new Pixel(x, y);
            let trimmed = false;
            // No double points.
            let points = new Set();
            // Lower edge
            let x_pair = outer.solve_x(y);
            if (x_pair) {
                let x0 = x_pair[0];
                let x1 = x_pair[1];
                if (Math.abs(x0 - x1) > eps) {
                    if (x0 >= x && x0 <= x+1) {
                        points.add([x0, y]);
                    }
                    if (x1 >= x && x1 <= x+1) {
                        points.add([x1, y]);
                    }
                }
            }
            // Right edge
            let y_pair = outer.solve_y(x+1.);
            if (y_pair) {
                let y0 = y_pair[0];
                let y1 = y_pair[1];
                if (Math.abs(y0 - y1) > eps) {
                    if (y0 >= y && y0 <= y+1) {
                        points.add([x+1., y0]);
                    }
                    if (y1 >= y && y1 <= y+1) {
                        points.add([x+1., y1]);
                    }
                }
            }
            // Upper edge
            x_pair = outer.solve_x(y+1.);
            if (x_pair) {
                let x0 = x_pair[0];
                let x1 = x_pair[1];
                if (Math.abs(x0 - x1) > eps) {
                    if (x0 >= x && x0 <= x+1) {
                        points.add([x0, y+1.]);
                    }
                    if (x1 >= x && x1 <= x+1) {
                        points.add([x1, y+1.]);
                    }
                }
            }
            // Left edge
            y_pair = outer.solve_y(x);
            if (y_pair) {
                let y0 = y_pair[0];
                let y1 = y_pair[1];
                if (Math.abs(y0 - y1) > eps) {
                    if (y0 >= y && y0 <= y+1) {
                        points.add([x, y0]);
                    }
                    if (y1 >= y && y1 <= y+1) {
                        points.add([x, y1]);
                    }
                }
            }

            if (points.size >= 2) {
                // To be honest, it's a huge pain to account for
                // situtations other than a pair, and it will not 
                // likely make a huge difference.
                let l = Array.from(points);
                p.trim_outer(l[0], l[1]);
                trimmed = true;
            }

            // Repeat for inner vertices.
            points.clear();
            // Lower edge
            x_pair = inner.solve_x(y);
            if (x_pair) {
                let x0 = x_pair[0];
                let x1 = x_pair[1];
                if (Math.abs(x0 - x1) > eps) {
                    if (x0 >= x && x0 <= x+1) {
                        points.add([x0, y]);
                    }
                    if (x1 >= x && x1 <= x+1) {
                        points.add([x1, y]);
                    }
                }
            }
            // Right edge
            y_pair = inner.solve_y(x+1.);
            if (y_pair) {
                let y0 = y_pair[0];
                let y1 = y_pair[1];
                if (Math.abs(y0 - y1) > eps) {
                    if (y0 >= y && y0 <= y+1) {
                        points.add([x+1., y0]);
                    }
                    if (y1 >= y && y1 <= y+1) {
                        points.add([x+1., y1]);
                    }
                }
            }
            // Upper edge
            x_pair = inner.solve_x(y+1.);
            if (x_pair) {
                let x0 = x_pair[0];
                let x1 = x_pair[1];
                if (Math.abs(x0 - x1) > eps) {
                    if (x0 >= x && x0 <= x+1) {
                        points.add([x0, y+1.]);
                    }
                    if (x1 >= x && x1 <= x+1) {
                        points.add([x1, y+1.]);
                    }
                }
            }
            // Left edge
            y_pair = inner.solve_y(x);
            if (y_pair) {
                let y0 = y_pair[0];
                let y1 = y_pair[1];
                if (Math.abs(y0 - y1) > eps) {
                    if (y0 >= y && y0 <= y+1) {
                        points.add([x, y0]);
                    }
                    if (y1 >= y && y1 <= y+1) {
                        points.add([x, y1]);
                    }
                }
            }

            if (points.size >= 2) {
                // To be honest, it's a huge pain to account for
                // situtations other than a pair, and it will not 
                // likely make a huge difference.
                let l = Array.from(points);
                p.trim_inner(l[0], l[1]);
                trimmed = true;
            }

            if (trimmed) {
                pixels[[x, y]] = p;
            }
        }
    }

    return [[[min_x, min_y], [max_x, max_y]], pixels];
}

function render_raster(raster)
{
    let min_x = raster[0][0][0];
    let min_y = raster[0][0][1];
    let max_x = raster[0][1][0];
    let max_y = raster[0][1][1];
    let pixels = raster[1];
    let s = ''
    let y = max_y;
    while (y >= min_y) {
        let x = min_x;
        while (x <= max_x) {
            if ([x, y] in pixels) {
                let p = pixels[[x, y]];
                let a = p.poly.area();
                if (a < 0.25) {
                    s += ' ';
                } else if (a < 0.5) {
                    s += '.';
                } else if (a < 0.75) {
                    s += 'o';
                } else {
                    s += 'O';
                }
            } else {
                s += ' ';
            }
            x+=1.0;
        }
        y -= 1.0;
        s+='\n';
    }

    return s;
}

export { Pixel, Ellipse, raster_ellipse, render_raster };

