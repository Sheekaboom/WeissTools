function [val] = pi2num(pi_str)
    %@brief change a string with \pi (from num2pi) to a float value (i.e.
    %   evaluate it)
    %@param[in] pi_str - formatted pi string (e.g. '\pi/2')
    %@warning this does NOT perform string cleaning... undesired code could be
    %   passed and run with eval
    %@return float of number from pi string
    pi_eval = regexprep(pi_str,'\\pi','pi'); % get evaluatable thing from formatted string
    val = eval(pi_eval);
end

