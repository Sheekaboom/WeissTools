function [figure_handle] = format_plot(figure_handle,varargin);
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
        lines = findobj(ax,'type','line'); 
        for line_num=1:length(lines)
            myline = lines(line_num);
            set(myline,'LineWidth',line_width); %set linewidth
            %set line color and style together together for good working with both bw and color
            if(p.Results.changeLineStyleColor)
                set_unique_color_linestyle(myline,line_num);
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