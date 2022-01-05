function [figure_handle] = format_plot(figure_handle,varargin)
    % @brief function for consistently formatting plots
    % @param[in] figure_handle - handle of figure to format
    % @param[in] varargin - key/value pairs for input as follows:
    %   type - type of formatting to perform ('paper','poster' currently work)
    %   changeLineStyleColor - true or false on whether to change linestyle and
    %            color (default true)
    % @return formatted_figure_handle - handle of formatted figure
    
    %set up input parser
    p = inputParser;
    p.addParameter('type','paper');
    p.addParameter('changeLineStyleColor',true) %
    p.addParameter('setLineStyleColorArgs',{});
    p.parse(varargin{:});

    if(strcmp(p.Results.type,'paper')) %paper figure
        font_size = 24;
        title_font_mult = 1;
        line_width = 2;
    else
        font_size = 24;
        title_font_mult = 1;
        line_width = 2;
    end %settings if statement

    %go through each axis
    axes = findobj(figure_handle,'type','axes');
    for ax_num=1:length(axes)
        ax = axes(ax_num); %get the current axis
        %set axes text sizes
        set(ax,'FontSize',font_size); %font size
        set(ax,'TitleFontSizeMultiplier', title_font_mult); %title multiplier
        %go through each line
        line_like = findobj(ax,'type','Line'); %objects that can use set_unique_color_linestyle
        line_like = [line_like; findobj(ax,'type','ErrorBar')];
        line_like = [line_like; findobj(ax,'type','Stem')];
        line_like = [line_like; findobj(ax,'type','Scatter')];
        for line_num=1:length(line_like)
            myline = line_like(line_num);
            set(myline,'LineWidth',line_width); %set linewidth
            if isgraphics(myline,'Stem') %if its a stem also set marker size
                set(myline,'MarkerSize',15);
            end
            if isgraphics(myline,'Scatter') % if its a scatter plot set the sizes
                set(myline,'LineWidth',3);
                set(myline,'SizeData',100);
            end
            %set line color and style together together for good working with both bw and color
            if(p.Results.changeLineStyleColor) && ~isgraphics(myline,'Scatter')
                set_unique_color_linestyle(myline,line_num,p.Results.setLineStyleColorArgs{:});
            end
        end %line_loop
        %go through polygons
        polys = findobj(ax,'type','polygon');
        for poly_num=1:length(polys)
            mypoly = polys(poly_num);
            set(mypoly,'LineWidth',line_width);
        end %poly loop
    end %axis loop
end %function

function [ line_handle ] = set_unique_color_linestyle( line_handle, seed,varargin)
%SET_UNIQUE_COLOR_LINESTYLE set the line given from line_handle with a
%unique color and linestyle (including marker types as linestyles) given by
%the seed value
p = inputParser;
p.addParameter('setColor',true);
p.addParameter('setLineStyle',true);
p.addParameter('setMarker',true);
p.parse(varargin{:});

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
if p.Results.setColor
    set(line_handle,'Color',colors(mod(seed-1,length(colors))+1,:));
end
if p.Results.setLineStyle
    set(line_handle,'LineStyle',ls_cell{mod(seed-1,length(ls_cell))+1});
end
if p.Results.setMarker
    set(line_handle,'Marker',mk_cell{mod(seed-1,length(mk_cell))+1});
end
end



