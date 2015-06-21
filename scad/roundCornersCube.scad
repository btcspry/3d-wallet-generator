module createMeniscus(h,radius)difference(){translate([radius/2+0.1,radius/2+0.1,0]){cube([radius+0.2,radius+0.1,h+0.2],center=true);}cylinder(h=h+0.2,r=radius,center=true);}
module roundCornersCube(x,y,z)translate([x/2,y/2,z/2]){difference(){r=((x+y)/2)*0.052;cube([x,y,z],center=true);translate([x/2-r,y/2-r]){rotate(0){createMeniscus(z,r);}}translate([-x/2+r,y/2-r]){rotate(90){createMeniscus(z,r);}}translate([-x/2+r,-y/2+r]){rotate(180){createMeniscus(z,r);}}translate([x/2-r,-y/2+r]){rotate(270){createMeniscus(z,r);}}}}