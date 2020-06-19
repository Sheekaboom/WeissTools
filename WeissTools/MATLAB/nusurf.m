function [fig] = nusurf(x,y,z,varargin)
%NUSURF Plot a surface from non-uniform data
%@param[in] x - x data
%@param[in] y - y data
%@param[in] z - z data
%@note Parameters should be passed like surf(...)
%@cite https://blogs.mathworks.com/videos/2007/11/02/advanced-matlab-surface-plot-of-nonuniform-data/
%@return surface plot handle

%% First create our meshgrid
%save a bit of memory from vectorized version
%xdist = abs(x-x');
xdist_min = inf;
for ix=1:length(x)
    xd = abs(x(ix)-x);
    xd_min = min(xd(xd~=0));
    xdist_min = min([xd_min,xdist_min]);
end
%ydist = abs(y-y');
ydist_min = inf;
for iy=1:length(y)
    yd = abs(y(iy)-y);
    yd_min = min(yd(yd~=0));
    ydist_min = min([yd_min,ydist_min]);
end
xgrid = min(x):xdist_min:max(x);
ygrid = min(y):ydist_min:max(y);
[X,Y] = meshgrid(xgrid,ygrid);

%% Now use grid data to get the values
Z = griddata(x,y,z,X,Y,'cubic');

%% Finally plot the values
fig = surf(X,Y,Z,varargin{:});

end

