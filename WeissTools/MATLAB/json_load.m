%% Function to load json
function data = json_load(path)
    %@brief load a json file given by path
    %@cite https://www.mathworks.com/matlabcentral/answers/326764-how-can-i-read-a-json-file
    fid = fopen(path); 
    raw = fread(fid,inf); 
    str = char(raw'); 
    fclose(fid); 
    data = jsondecode(str);
end