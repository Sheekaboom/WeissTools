function set_pi_axis(ax,interval,xyz)
%@brief take an axis and label in increments of pi
%@param[in] ax - axis to set pi on
%@param[in] interval - interval to put ticks on (e.g. pi/2). 
%   Should be expressed in terms of a multiple of pi
%@param[in] xyz - chararray with single or combo of 'x','y','z'
% to specify which direction of the axis to set

    for i=1:length(xyz) %go through each letter
        
        dchar = upper(xyz(i));
        lims = get(ax,sprintf('%cLim',dchar));

        %start at 0 to always include 0
        ticks = lims(1):interval:lims(2);
        ticks = ticks - ticks(find(ticks==min(abs(ticks))));

        %Now set the tick values
        set(ax,sprintf('%cTick',dchar),ticks);
        
        %And the tick labels
        [n,d] = rat(ticks/pi); %get fractions in terms of pi
        tick_str = strcat(string(n),'\pi/',string(d));
        tick_str{n==0} = '0'; %fix 0
        %now fix some formatting things
        for s=1:length(tick_str)
            tick_str(s) = regexprep(tick_str(s),'1\\pi','\\pi'); %replace 1\pi
            tick_str(s) = regexprep(tick_str(s),'/1',''); %remove div by 1
        end
        ticklabels = cellstr(tick_str);
        set(ax,sprintf('%cTickLabels',dchar),ticklabels);
        %set(ax,'TickLabelInterpreter','latex');
   
    end
    
end

%{
%Test case
x = linspace(-pi,pi,100);
y = cos(x);
plot(x,y);
set_pi_axis(gca,pi/2,'x');
%}