
class Vector2d {
    constructor(x, y)
    {
        this.x = x;
        this.y = y;
    }

    // Counter clockwise normal
    normal()
    {
        return new Vector2d(-this.y, this.x)
    }

    dot(v)
    {
        console.assert((typeof v == 'object') && (v instanceof Vector2d),
          'bad type argument to dot()');
        return this.x * v.x + this.y * v.y
    }

    print()
    {
        console.log('<' + this.x.toString() + ', ' + this.y.toString() + '>');
    }
}

// As always, counterclockwise.
class HalfSpace {
    constructor(start, end)
    {
        console.assert((typeof start == 'object') && (Array.isArray(start)),
          'start must be an array');
        console.assert(start.length >= 2, 'Not enough coordinates in start');
        console.assert((typeof end == 'object') && (Array.isArray(end)),
          'end must be an array');
        console.assert(end.length >= 2, 'Not enough coordinates in end');
        this.point = start;
        let v = new Vector2d(end[0] - start[0], end[1] - start[1]);
        this.alt_point = end;
        this.normal = v.normal();
    }

    contains(p)
    {
        console.assert((typeof p == 'object') && (Array.isArray(p)),
          'p must be an array');
        console.assert(p.length >= 2, 'Not enough coordinates in p');
        let test = new Vector2d(p[0] - this.point[0],
          p[1] - this.point[1]);
        return this.normal.dot(test) >= 0;
    }

    intersection(start, end)
    {
        console.assert((typeof start == 'object') && (Array.isArray(start)),
          'start must be an array');
        console.assert(start.length >= 2, 'Not enough coordinates in start');
        console.assert((typeof end == 'object') && (Array.isArray(end)),
          'end must be an array');
        console.assert(end.length >= 2, 'Not enough coordinates in end');
        let v0 = new Vector2d(start[0] - this.point[0],
          start[1] - this.point[1]);
        let v1 = new Vector2d(end[0] - this.point[0],
          end[1] - this.point[1]);
        let q = v0.dot(this.normal);
        let r = v1.dot(this.normal);
        if (q-r == 0) {
            return None;
        }
        let t = 1.*q / (q-r);
        let v = new Vector2d(end[0] - start[0], end[1] - start[1]);
        return [start[0] + t*v.x, start[1] + t*v.y];
    }
}

// I got the area equation from here:
// https://www.mathwords.com/a/area_convex_polygon.htm

// Important is this assumes a counterclockwise convention for positive
// area. If you reverse the ordering, the areas will be negative.
class ConvexPolygon {
    constructor(vertices)
    {
        console.assert((typeof vertices == 'object') && Array.isArray(vertices),
            'vertices must be an array.');
        vertices.forEach(item =>
            console.assert((typeof item == 'object') && Array.isArray(item),
                'items in vertices must be arrays') );
        vertices.forEach(item =>
            console.assert(item.length >= 2,
                'items in vertices must have two coordinates.'));
        this.vertices = vertices;
    }

    edge_count()
    {
        return this.vertices.length;
    }

    get_vertex(i)
    {
        return this.vertices[i];
    }

    area()
    {
        let pos_diag_sum = 0.0;
        let neg_diag_sum = 0.0;
        let m = this.vertices.length;
        let v = this.vertices;
        for (let i = 0; i < m; ++i) {
            let k = i + 1;
            if (k >= m) {
                k = 0;
            }
            pos_diag_sum += v[i][0] * v[k][1];
            neg_diag_sum += v[i][1] * v[k][0];
        }
        return (pos_diag_sum - neg_diag_sum) / 2.0;
    }

    trim(start, end)
    {
        console.assert((typeof start == 'object') && (Array.isArray(start)),
          'start must be an array');
        console.assert(start.length >= 2, 'Not enough coordinates in start');
        console.assert((typeof end == 'object') && (Array.isArray(end)),
          'end must be an array');
        console.assert(end.length >= 2, 'Not enough coordinates in end');
        let h = HalfSpace(start, end);
        let in_v = this.vertices;
        let out_v = [];
        for (let i = 0; i < in_v.length; ++i) {
            let cur_point = in_v[i];
            let prev_point = undefined;
            if (i == 0) {
                prev_point = in_v[in_v.length - 1];
            } else {
                prev_point = in_v[i-1];
            }
            if (h.contains(cur_point)) {
                if (!h.contains(prev_point)) {
                    out_v.push(h.intersection(prev_point, cur_point));
                }
                out_v.push(cur_point);
            } else if (h.contains(prev_point)) {
                out_v.push(h.intersection(prev_point, cur_point))
            }
        }

        this.vertices = out_v;
    }
}

export { Vector2d, HalfSpace, ConvexPolygon };
