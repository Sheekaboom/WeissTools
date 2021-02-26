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

%% Lets attempt to figure out subplots
% @note this still isn't fully implemented. Will require quite a bit more
% work... not gonna do it right now. I'll just do it manually
ax_info = get_axes_layout_plotly(json_data.layout);

for axi=1:ax_info.count
    subplot(ax_info.count,1,axi); grid on; hold on;
end


%% now lets plot
for di=1:length(json_data.data) % loop through each trace
    % Handle in case its a cell array (sometimes it is)
    if iscell(json_data.data)
        trace_data = json_data.data{di};
    else 
        trace_data = json_data.data(di);
    end
    % check if we are a subplot and set our subplot
    if ax_info.count>1
       ax_num = find(strcmp(trace_data.yaxis,ax_info.x.anchors)); % plotly anchors axes to y always, so we take y
       subplot(ax_info.count,1,ax_num)
    end
    plot_type = trace_data.type;
    %extract error bar if they exist
    if isfield(trace_data,'error_y')
        error_y = [trace_data.error_y]; %extract the struct
        %error_y = {error_y(:).array}; %extract the data
        plot_type='errorbar';
    end
    
    plot_kwargs = {'DisplayName',trace_data.name};
    switch plot_type
        case 'bar' % bar plot
            bar(trace_data.x,trace_data.y,1,plot_kwargs{:});
            
        case 'scatter' %simple line plot
            % now check the modes
            trace_mode = 'lines'; % default mode
            if isfield(trace_data,'mode'); trace_mode = trace_data.mode; end
            % switch for future extension
            switch trace_mode
                case 'markers'
                    scatter(trace_data.x,trace_data.y,plot_kwargs{:})
                otherwise
                    plot(trace_data.x,trace_data.y,plot_kwargs{:}); %plot
            end
            
        case 'errorbar' %errorbar plot
            errorbar(trace_data.x,trace_data.y,error_y,plot_kwargs{:});
    end
end

%% Extract some layout information
if isfield(json_data.layout,'title')
    if isfield(json_data.layout.title,'text')
        title(json_data.layout.title.text);
    end
end

for axi=1:length(ax_info.y.names)
    fld = ax_info.y.names{axi};
    if isfield(ax_info.y.data.(fld),'title')
        ylabel(ax_info.y.data.(fld).title.text);
    end
end

for axi=1:length(ax_info.x.names)
    fld = ax_info.x.names{axi};
    if isfield(ax_info.x.data.(fld),'title')
        axtitle = ax_info.x.data.(fld).title.text;
        label_args = {};
        if islatex(axtitle) 
            axtitle = convert_latex(axtitle);
            label_args = [label_args,{'interpreter','latex'}]; 
        end
        xlabel(axtitle,label_args{:})
    end
end

%% Set xlims to max and min if not defined
for axi=1:ax_info.count
    subplot(ax_info.count,1,axi);
    ax = gca(); % get current axis
    cur_ax_info = ax_info.x.data.(ax_info.x.names{axi});
    if isfield(cur_ax_info,'range')
        myrange = cur_ax_info.range;
        xlim(myrange);
    end
end

%% Set ylims to max and min if not defined
for axi=1:ax_info.count
    subplot(ax_info.count,1,axi);
    ax = gca(); % get current axis
    cur_ax_info = ax_info.y.data.(ax_info.y.names{axi});
    if isfield(cur_ax_info,'range') % only set if defined. Otherwise auto
        myrange = cur_ax_info.range;
        axmin = myrange(1); axmax = myrange(2);
        ylim(myrange); 
    end
end

%% Turn on the legend
for axi=1:ax_info.count
    subplot(ax_info.count,1,axi);
    legend('show','location','best');
end

        
end


function [tf] = islatex(str)
    % @brief test whether a string is latex or not (checks $ at beginning
    %   and end)
    % @param[in] str - string to check (usually an axis_title or title)
    % @return boolean whether we think its latex or not
    str = strip(str); % strip whitespace
    tf = all([str(1)=='$',str(end)=='$']);
end

function [mtex] = convert_latex(tex)
    % @brief convert a latex string to MATLAB compatable. (some things not
    %   supported e.g. \text flag
    % @param[in] tex - string to convert
    % @return reformatted latex string for MATLAB
    mtex = tex; % init
    % Lets deal with \text flags that MATLAB can't handle
    [re_start,re_end] = regexp(tex,'\\text\{[\w\d\s\)\(\,\.\+\-\*\\\/]+\}');
    for i=1:length(re_start)
        full_str = tex(re_start(i):re_end(i));
        text = [strrep(full_str(1:end-1),'\text{','$'),'$'];
        mtex = strrep(mtex,full_str,text);
    end
    % remove any empty math sections
    mtex = strrep(mtex,'$$','');
end
    
        
function [axinfo] = get_axes_layout_plotly(layout)
    % @brief take a plotly layout and try to extract axes information
    % @param[in] layout - layout field of plotly json data
    % @return struct with x,y fields with varying information and some
    % other fields like count for number of axes
    axinfo = struct();
    axinfo.x = struct();
    axinfo.y = struct();
    layout_fields = fields(layout);
    % get the axes structs themselvs
    axinfo.x.data = struct();
    axinfo.y.data = struct();
    axinfo.x.data_enum = {};
    axinfo.y.data_enum = {};
    for fi=1:length(layout_fields)
        fld = layout_fields{fi};
        if startsWith(fld,'xaxis')
            axinfo.x.data.(fld) = layout.(fld);
            axinfo.x.data_enum{end+1} = layout.(fld);
        elseif startsWith(fld,'yaxis')
            axinfo.y.data.(fld) = layout.(fld);
            axinfo.y.data_enum{end+1} = layout.(fld);
        end
    end
    % now extract useful data
    axinfo.x.names = fields(axinfo.x.data);
    axinfo.y.names = fields(axinfo.y.data);
    % get the anchor names
    axinfo.x.anchors = cell(1,length(axinfo.x.names));
    for axi=1:length(axinfo.x.anchors)
        if isfield(axinfo.x.data.(axinfo.x.names{axi}),'anchor')
            axinfo.x.anchors{axi} = axinfo.x.data.(axinfo.x.names{axi}).anchor;
        else
            axinfo.x.anchors{axi} = 'y';
        end
    end
    % assume number of x axes = num subplots
    axinfo.count = length(axinfo.x.anchors); 
end    


%{
%testing code
json_path = "C:\Users\aweis\Google Drive\GradWork\papers\2019\python-matlab\data\figs\plotly\json\combo.json";
pfig = plotly2fig(json_path)
%}
