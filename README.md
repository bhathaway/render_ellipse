# render_ellipse
ASCII art ellipse renderer

## Purpose
I enjoy playing Minecraft with my sons, and frequently use circle and ellipse generators
to help with design. What is missing from tools that I've found is the ability to rotate ellipses,
use fractional radii, and further be able to nudge the ellipse for the best possible pixelation.
In addition, Mincraft has slab and stair blocks that many have used to help get the appearance of
higher resolution. So I've also sought to address that in this project by way of quartile representation.

The reason I've titled this **ASCII art ellipse renderer** is because I've of course realized that the tool I've
created has broader use than just Minecraft. I rather like some of the text output I've seen.

## Target Technologies
The main technologies I've chosen to use are _python_ , _c++_ and _JavaScript_. _python_ is excellent for command line
usage and testing, whereas the _JavaScript_ is basically the only option for client-side execution. I would like to
eventually create a full webapp for this tool to give back to the community.

## Theory
For better or worse, this project revolves around the general ellipse equation adapted for rotation about an
angle. Solving for X and Y intercepts is a core problem that has a closed form solution. There are two main ideas
I could think of for rendering. The first, and most obvious, is to subsample the pixels in some regular pattern
to decide the coverage. The second is to model the pixels and use the intercepts of the ellipse edges with the pixels
to create simple convex polygons to get a fairly precise estimate of the area. This was the approach I chose, though
at some point I may add the former approach since it is more straightforward to understand and, while less accurate,
could have far fewer corner cases to consider.

## Current State
As I mentioned, there are some corner cases. I think I've covered them fairly well with the manual testing that I've
set up, but further use may reveal unseen issues.

## Future Work
* Why not add the simpler method and compare performance?
* Instead of resolving the intercepts in the algorithm, cache them.
