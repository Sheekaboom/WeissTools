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
x_vals = {json_data.data.x}; %get x values
y_vals = {json_data.data.y}; %get y values
names  = {json_data.data.name}; %get our names

plot_type='line'; %assume its a line plot here

%extract error bar if they exist
if isfield(json_data.data,'error_y')
    error_y = [json_data.data.error_y]; %extract the struct
    error_y = {error_y(:).array}; %extract the data
    plot_type='errorbar';
end
    
%% now lets plot
switch plot_type
    case 'line' %simple line plot
        for di=1:length(x_vals)
            plot(x_vals{di},y_vals{di},...
                'DisplayName',names{di}); %plot
        end
    case 'errorbar' %errorbar plot
        for di=1:length(x_vals)
            errorbar(x_vals{di},y_vals{di},...
                error_y{di},'DisplayName',names{di});
        end
end

%% Extract some layout information
if isfield(json_data.layout.title,'text')
    title(json_data.layout.title.text);
end
if isfield(json_data.layout.yaxis,'title')
    ylabel(json_data.layout.yaxis.title.text);
end
if isfield(json_data.layout.xaxis,'title')
    xlabel(json_data.layout.xaxis.title.text);
end

%% Turn on the legend
legend('show','location','best');
        
end


%{
%testing code
json_path = "C:\Users\aweis\Google Drive\GradWork\papers\2019\python-matlab\data\figs\plotly\json\combo.json";
pfig = plotly2fig(json_path)
%}
