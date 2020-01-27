function [ ] = save_plot( fig_handle,name,fig_folder,varargin)
% @brief pass a figure handle, name, and fig folder and plot in specific formats
% @param[in] fig_handle - handle to the figure to save
% @param[in] name - name (without extension) of figures to save
% @param[in] fig_folder - folder to save our figures to
% @param[in/OPT] name/value pairs are as follows:
%   figureLocation - figure location in [x_start,y_start,x_len,y_len] in
%       inches ('none' will keep the current position)
%   figureUnits    - units for the figure (defaults to Inches)
%   saveTypes      - cell array of types to save (png,epsc,jpg,fig,emf,tiff,svg,...,etc)
%   formatPlot     - whether or not to format plot 
%            (default is true. false will prevent formatting)

%input parsing
p = inputParser; 
p.addParameter('figureLocation',[2,2,7,5]);
p.addParameter('figureUnits','Inches')
p.addParameter('formatPlot',true)
p.addParameter('saveTypes',{'png','epsc','jpg','fig','emf','tiff','svg'});
p.parse(varargin{:});

save_types      = p.Results.saveTypes;
figure_location = p.Results.figureLocation;
figure_units    = p.Results.figureUnits;
format_plot_flg = p.Results.formatPlot;

if format_plot_flg
    fig_handle = format_plot(fig_handle);
end

if strcmp(figure_location,'none')
    figure_location = get(fig_handle,'position');
end

set(fig_handle, 'Units', figure_units, 'Position', figure_location);

%legend('show','location','best');
%legh = findobj(fig_handle,'Type','Legend');
%set(legh,'Location','best');
%legend(legh,'Location','best')
for type=save_types
    %create the folder if it doesnt exist
    t = type{1};
    fig_path = fullfile(fig_folder,t);
    if(~exist(fig_path))
        mkdir(fig_path);
    end
    %now save
    fig_save_path = char(fullfile(fig_path,name));
    saveas(fig_handle,fig_save_path,t);
end

