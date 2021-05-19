function [fig] = set_positive_theta(fig,phi)
    %@brief take a figure with x axis of theta values and change any negative
    % values to positive and add coresponding phi values to the plot
    %@param[in] fig - figure handle with theta values on x axis
    %   Detailed explanation goes here
    %@param[in/OPT] phi - phi value the plot is at (typically 0)
    %@note this just changes the labels. The values must stay otherwise the
    %   plot will start looking weird (cant have multiple positives)
    %return updated figure with phi labels and positive theta labels
    arguments
        fig;
        phi double = 0;
    end

    %% Now lets change the labels and add a line
    axes = findobj(fig,'type','axes'); % get the axes
    for axi=1:length(axes)
        % get the axis
        ax = axes(axi);
        % add a vertical line at 0
        yl = ax.YLim; 
        plot(ax,[0,0],yl,'color','black','HandleVisibility','off');
        ylim(yl)
        % set new x tick values
        xta = abs(ax.XTick); % get absolute value (no negative)
        xtlabels = arrayfun(@(x) num2pi(x),xta,'UniformOutput',false); % get the new labels
        ax.XTickLabel = xtlabels; % set new labels
    end
    %% add the phi labels
    phi_vals = {num2pi(pi-phi),num2pi(phi)}; % strings for phi labels
    phi_annot_left = annotation('textbox',[0.1,1,.4,.02],...
        'HorizontalAlignment','right','VerticalAlignment','top',...
        'String',['\leftarrow\phi=',phi_vals{1},''],...
        'EdgeColor','none','FontSize',24);
    phi_annot_right = annotation('textbox',[0.55,1,.4,.02],...
        'HorizontalAlignment','left','VerticalAlignment','top',...
        'String',['\phi=',phi_vals{2},'\rightarrow'],...
        'EdgeColor','none','FontSize',24);
end


%{
% Example
updated_fig = set_positive_theta(fig)
%}

