function [ line_handle ] = set_unique_color_linestyle( line_handle, seed )
%SET_UNIQUE_COLOR_LINESTYLE set the line given from line_handle with a
%unique color and linestyle (including marker types as linestyles) given by
%the seed value
%set our color list
colors = ([ 0  ,50 ,135; 200,20 ,30 ; 0  ,120,0  ; 120,90 ,0  ;...
            150,50 ,165; 10 ,145,120; 0  ,0  ,0  ; 220,150,20 ;...
            200,150,200; 255,255,0  ; 255,0  ,128; 150,150,0  ;...
            0  ,255,255; 0  ,255,0  ; 255,80  ,255]/255);

%and set our lienstyles
%this should provide 52 unique linestyle/marker pairs
linestyles = '-|--|:|-.';
markers    = '.|+|o|*|x|s|d|^|v|>|<|p|h'; %first one
ls_cell = repmat(strsplit(linestyles,'|'),1,4);
mk_cell = strsplit(markers,'|');

%set the values onto the line
set(line_handle,'Color',colors(mod(seed-1,length(colors))+1,:),...
    'LineStyle',ls_cell{mod(seed-1,length(ls_cell))+1},...
    'Marker',mk_cell{mod(seed-1,length(mk_cell))+1});

end

