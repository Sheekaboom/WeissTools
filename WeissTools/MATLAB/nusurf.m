function [fig] = nusurf(x,y,z,varargin)
%NUSURF Plot a surface from non-uniform data
%@param[in] x - x data
%@param[in] y - y data
%@param[in] z - z data
%@note Parameters should be passed like surf(...)
%@cite https://blogs.mathworks.com/videos/2007/11/02/advanced-matlab-surface-plot-of-nonuniform-data/
%@return surface plot handle

%% First create our meshgrid
xdist = abs(x-x');
ydist = abs(y-y');
xgrid = min(x):min(xdist(xdist~=0)):max(x);
ygrid = min(y):min(ydist(ydist~=0)):max(y);
[X,Y] = meshgrid(xgrid,ygrid);

%% Now use grid data to get the values
Z = griddata(x,y,z,X,Y,'cubic');

%% Finally plot the values
fig = surf(X,Y,Z,varargin{:});

end

