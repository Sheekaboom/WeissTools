function [latex_str] = matrix2latex(A)
%MATRIX2LATEX Covnert a matrix to latex
% @param[in] A - matrix to convert
% @note assumes asmmath is enabled
env_name   = 'bmatrix'; %environment to open
pre_text   = ''; %text to go before begin envioronment (e.g. left)
post_text  = ''; %text to go after end environment (e.g. right)
arg_text   = ''; %text to go right after begin environ(e.g. {ccc})
format_str = '%5.3G'; %string for formatting numbers
%beginning and ends to environments
begin_str = sprintf('%s\\begin{%s}%s ',pre_text,env_name,arg_text);
end_str   = sprintf(' \\end{%s}%s',env_name,post_text);
%now lets create our data
data_str = '';
for i=1:size(A,1)
    %concatenate all the data
    data_str = strcat(data_str,strip(sprintf('%5.3G&',A(i,:)),'&'));
    if i~=size(A,1)
        data_str = strcat(data_str,' \\ ');
    end
end
latex_str = strcat(begin_str,data_str,end_str);
end


