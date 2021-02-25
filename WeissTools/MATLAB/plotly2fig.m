function [fig_handle] = plotly2fig(plotly_file)
%@brief Take in a json description of a plotly plot and change
% it to a MATLAB figure
%@param[in] plotly_file - path to plotly generated json file
%@param[in/OPT] varargin - key/val pairs as follows: 
%   - None - Yet!
%@cite https://www.mathworks.com/matlabcentral/answers/183984-is-any-change-displayname-property-in-plot-function
%@return figure handle to generated figure

%% first load the json data
json_path = plotly_file;
fid = fopen(json_path);  %open the json file
raw = fread(fid,inf); %read the data
str = char(raw'); 
fclose(fid); %close the file
json_data = jsondecode(str); %decode the data

%% initialize our figure
fig_handle = figure(); hold on; grid on;

%% now lets extract the data
%this is done in cell arrays becaues the traces dont have to be
% the same length as one another.
%x_vals = {json_data.data.x}; %get x values
%y_vals = {json_data.data.y}; %get y values
%names  = {json_data.data.name}; %get our names
%types  = {json_data.data.type};

%plot_type='line'; %assume its a line plot here
    
%% now lets plot
for di=1:length(json_data.data) % loop through each trace
    trace_data = json_data.data{di};
    plot_type = trace_data.type;
    %extract error bar if they exist
    if isfield(trace_data,'error_y')
        error_y = [trace_data.error_y]; %extract the struct
        %error_y = {error_y(:).array}; %extract the data
        plot_type='errorbar';
    end
    switch plot_type
        case 'bar' % bar plot
            bar(trace_data.x,trace_data.y,1,...
                'DisplayName',trace_data.name);
        case 'scatter' %simple line plot
            plot(trace_data.x,trace_data.y,...
                'DisplayName',trace_data.name); %plot
        case 'errorbar' %errorbar plot
            errorbar(trace_data.x,trace_data.y,...
                error_y,'DisplayName',trace_data.name);
    end
end

%% Extract some layout information
if isfield(json_data.layout,'title')
    if isfield(json_data.layout.title,'text')
        title(json_data.layout.title.text);
    end
end
if isfield(json_data.layout,'yaxis')
    if isfield(json_data.layout.yaxis,'title')
        ylabel(json_data.layout.yaxis.title.text);
    end
end
if isfield(json_data.layout,'xaxis')
    if isfield(json_data.layout.xaxis,'title')
        xlabel(json_data.layout.xaxis.title.text);
    end
end

%% Set xlims to max and min
ax = findall(fig_handle,'type','axes');
ax = ax(1); % for future use with subplots
axmin=inf;axmax=-inf; % init
% get max/min from all axis traces
for li=1:length(ax.Children)
    cmax = max(ax.Children(li).XData);
    cmin = min(ax.Children(li).XData);
    if cmax>axmax; axmax=cmax; end
    if cmin<axmin; axmin=cmin; end
end
xlim([axmin,axmax]);

%% Turn on the legend
legend('show','location','best');
        
end


%{
%testing code
json_path = "C:\Users\aweis\Google Drive\GradWork\papers\2019\python-matlab\data\figs\plotly\json\combo.json";
pfig = plotly2fig(json_path)
%}
