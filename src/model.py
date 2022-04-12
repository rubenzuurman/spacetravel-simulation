import os

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image
import pyrr

import logger as lg

class Model:
    """
    Model class loading an obj file and a texture file and loading the data 
    into GPU memory. Also facilitates binding of buffers and rendering.
    
    Vertex positions are defined by 3 or 4 floats (only 3 is supported) by
        `v x y z [w=1.0]`.
    Texture coordinates are defined by 1, 2, or 3 floats (only 2 is supported) in the interval [0, 1] by
        `vt u [v=0.0 [w=0.0]]`.
    Vertex normals are defined by 3 floats by
        `vn x y z`.
    Faces are defined by 3 or more vertex specifications by
        `f spec1 spec2 spec3 ...`.
        A vertex specification consists of the vertex index, the optional 
        texture coordinate, and the optional vertex normal. A specification is
        of the form `vertex_index[/texture_index][/normal_index]`. When the 
        normal index is included but the texture index is not, the slash in 
        front of the texture index should be included anyway.
        Faces with more than 3 vertices will be split by using the following 
        pattern: (1 2 3) (1 3 4) ... (1 n-2 n-1) (1 n-1 n).
    Groups (defined by `g`), more than one object (defined by `o`), parameter 
        space vertices (defined by `vp`), smooth shading (defined by `s`), and
        line elements (defined by `l`) are all not supported and will be 
        ignored. A warning will be printed upon first encounter (on second 
        encounter for objects).
    """
    
    def __init__(self, logger):
        """
        Initialize vertex_data and index_data.
        """
        # Initialize logger.
        self.logger = logger
        
        # Initialize vertex_data and index_data.
        self.vertex_data = None
        self.index_data = None
        
        # Initialize name, will be set in the function
        # get_vertex_and_index_arrays().
        self.name = ""
    
    def get_model_file_contents(self, path):
        """
        Checks if the path exists and is a file. Checks if the file contents 
        are fomatted correctly. Returns a list of the lines in the file.
        """
        # Check if the path exists and if the path is a file.
        if not os.path.exists(path):
            raise Exception(f"File does not exists: {path}")
        if not os.path.isfile(path):
            raise Exception(f"File does not exists: {path}")
        
        # Get file contents.
        with open(path, "r") as file:
            lines = file.readlines()
        
        # Remove leading and trailing spaces/newlines.
        lines = [line.strip() for line in lines]
        
        # Replace all tabs with spaces.
        for index in range(len(lines)):
            if "\t" in lines[index]:
                lines[index] = lines[index].replace("\t", " ")
        
        # Replace all multiples of consecutive spaces with single spaces.
        for index in range(len(lines)):
            while "  " in lines[index]:
                lines[index] = lines[index].replace("  ", " ")
        
        # Variable for printing warnings for commands which are not supported.
        group_warning_printed = False
        multiple_objects_warning_printed = False
        object_encountered = False
        parameter_space_vertex_warning_printed = False
        smooth_shading_warning_printed = False
        line_element_warning_printed = False
        
        # Loop over lines to check data format.
        for index, line in enumerate(lines):
            # Skip empty lines.
            if line == "":
                continue
            
            # Skip comments.
            if line.startswith("#"):
                continue
            
            # Split line and calculate argument count.
            line_split = line.split(" ")
            arg_count = len(line_split) - 1
            
            if line_split[0] == "v":
                # Check argument count.
                #if not (arg_count >= 3 and arg_count <= 4):
                if not arg_count == 3: # For only x y z coords.
                    self.logger.log(f"Error in {path}:{index+1}: Invalid " \
                        f"number of arguments for `v`: {arg_count} " \
                        "(expected 3 or 4).")
                    return False
                # Check castable to float.
                for arg in line_split[1:]:
                    try:
                        f = float(arg)
                    except Exception as e:
                        self.logger.log(f"Error in {path}:{index+1}: Value " \
                            f"of `{arg}` is not a float.")
                        return False
            elif line_split[0] == "vt":
                # Check argument count.
                #if not (arg_count >= 1 and arg_count <= 3):
                if not arg_count == 2: # For only u v coords.
                    self.logger.log(f"Error in {path}:{index+1}: Invalid " \
                        f"number of arguments for `vt`: {arg_count} " \
                        "(expected 1, 2, or 3).")
                    return False
                # Check castable to float.
                for arg in line_split[1:]:
                    try:
                        f = float(arg)
                    except Exception as e:
                        self.logger.log(f"Error in {path}:{index+1}: Value " \
                            f"of `{arg}` is not a float.")
                        return False
                # Check between 0 and 1.
                for arg in line_split[1:]:
                    f = float(arg)
                    if not (f >= 0 and f <= 1):
                        self.logger.log(f"Error in {path}:{index+1}: Value " \
                            f"of `{arg}` for vt must be contained by the " \
                            "interval [0, 1].")
                        return False
            elif line_split[0] == "vn":
                # Check argument count.
                if not arg_count == 3:
                    self.logger.log(f"Error in {path}:{index+1}: Invalid " \
                        f"number of arguments for `vn`: {arg_count} " \
                        "(expected 3).")
                    return False
                # Check castable to float.
                for arg in line_split[1:]:
                    try:
                        f = float(arg)
                    except Exception as e:
                        self.logger.log(f"Error in {path}:{index+1}: Value " \
                            f"of `{arg}` is not a float.")
                        return False
            elif line_split[0] == "vp":
                # Warn the user because this is not supported at the moment.
                if not parameter_space_vertex_warning_printed:
                    self.logger.log(f"Warning in {path}:{index+1}: Parameter " \
                        "space vertices are not supported at the moment.")
                    parameter_space_vertex_warning_printed = True
                continue
            elif line_split[0] == "f":
                # Check argument counter.
                if not arg_count >= 3:
                    self.logger.log(f"Error in {path}:{index+1}: Invalid " \
                        f"number of arguments for `f`: {arg_count} " \
                        "(expected at least 3).")
                    return False
            elif line_split[0] == "g":
                # Warn the user because this is not supported at the moment.
                if not group_warning_printed:
                    self.logger.log(f"Warning in {path}:{index+1}: " \
                        "Groups are not supported at the moment.")
                    group_warning_printed = True
                continue
            elif line_split[0] == "o":
                if not object_encountered:
                    object_encounterd = True
                    continue
                if not multiple_objects_warning_printed:
                    self.logger.log(f"Warning in {path}:{index+1}: " \
                        "Multiple objects are not supported at the moment.")
                    multiple_objects_warning_printed = True
                continue
            elif line_split[0] == "s":
                # Warn the user because this is not supported at the moment.
                if not smooth_shading_warning_printed:
                    self.logger.log(f"Warning in {path}:{index+1}: Smooth " \
                        "shading is not supported at the moment.")
                    smooth_shading_warning_printed = True
                continue
            elif line_split[0] == "l":
                # Warn the user because this is not supported at the moment.
                if not line_element_warning_printed:
                    self.logger.log(f"Warning in {path}:{index+1}: Line " \
                        "elements are not supported at the moment.")
                    line_element_warning_printed = True
                continue
            else:
                # Warn the user of an unknown command.
                self.logger.log(f"Warning in {path}:{index+1}: Unknown " \
                    f"command {line_split[0]}.")
        
        # Count the number of vertices, texture coordinates, and vertex 
        # normals.
        num_of_verts = len([line for line in lines \
            if line.split(" ")[0] == "v"])
        num_of_texcoords = len([line for line in lines \
            if line.split(" ")[0] == "vt"])
        num_of_vert_normals = len([line for line in lines \
            if line.split(" ")[0] == "vn"])
        
        # Check if the vertices specified by faces exist.
        for index, line in enumerate(lines):
            line_split = line.split(" ")
            
            # Only evaluate faces.
            if not line_split[0] == "f":
                continue
            
            # Loop over face arguments.
            for arg in line_split[1:]:
                # If the argument starts or ends with a /, there was a space 
                # there before splitting.
                if arg.startswith("/") or arg.endswith("/"):
                    self.logger.log(f"Error in {path}:{index+1}: " \
                        "Slash in face definition cannot be preceded " \
                        "or followed by a space.")
                    return False
                
                # Get vertex index, texture coordinate index, and vertex 
                # normal index. Zero or empty string means not present.
                vertex_index = 0
                texture_coordinate_index = 0
                vertex_normal_index = 0
                
                vertex_index_str = ""
                texture_coordinate_index_str = ""
                vertex_normal_index_str = ""
                
                # Set strings.
                if not "/" in arg:
                    vertex_index_str = arg
                else:
                    # Get vertex index, texture coordinate index, and vertex 
                    # normal index from string.
                    arg_split = arg.split("/")
                    if len(arg_split) == 2:
                        vertex_index_str, texture_coordinate_index_str = arg_split
                    if len(arg_split) == 3:
                        vertex_index_str, texture_coordinate_index_str, vertex_normal_index_str = arg_split
                
                # Check if the vertex index string is empty.
                if vertex_index_str == "":
                    self.logger.log(f"Error in {path}:{index+1}: Vertex " \
                        "index must be specified.")
                    return False
                # Check if the vertex index string is castable to an integer.
                try:
                    n = int(vertex_index_str)
                except Exception as e:
                    self.logger.log(f"Error in {path}:{index+1}: Vertex " \
                        f"index must be an integer, not " \
                        f"`{vertex_index_str}`.")
                    return False
                vertex_index = n
                # Check if the vertex index exists.
                if vertex_index > 0:
                    if not vertex_index <= num_of_verts:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            f"Vertex with index {vertex_index} does not " \
                            "exist.")
                        return False
                elif vertex_index < 0:
                    if not vertex_index >= -num_of_verts:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            f"Vertex with index {vertex_index} does not " \
                            "exist.")
                        return False
                else:
                    self.logger.log(f"Error in {path}:{index+1}: Vertex " \
                        f"with index {vertex_index} does not exist.")
                    return False
                
                # Check if the texture coordinate index string is empty.
                if not texture_coordinate_index_str == "":
                    # Check if the texture coordinate index string is 
                    # castable to an integer.
                    try:
                        n = int(texture_coordinate_index_str)
                    except Exception as e:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            "Texture coordinate index must be an integer, " \
                            f"not `{texture_coordinate_index_str}`.")
                        return False
                    texture_coordinate_index = n
                    # Check if texture coordinate index exists.
                    if texture_coordinate_index > 0:
                        if not texture_coordinate_index <= num_of_texcoords:
                            self.logger.log(f"Error in {path}:{index+1}: " \
                                f"Texture coordinate with index " \
                                f"{texture_coordinate_index} does not exist.")
                            return False
                    elif texture_coordinate_index < 0:
                        if not texture_coordinate_index >= -num_of_texcoords:
                            self.logger.log(f"Error in {path}:{index+1}: " \
                                f"Texture coordinate with index " \
                                f"{texture_coordinate_index} does not exist.")
                            return False
                    else:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            f"Texture coordinate with index " \
                            f"{texture_coordinate_index} does not exist.")
                        return False
                
                # Check if the vertex normal index string is empty.
                if not vertex_normal_index_str == "":
                    # Check if the vertex normal index string is castable to 
                    # an integer.
                    try:
                        n = int(vertex_normal_index_str)
                    except Exception as e:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            "Vertex normal index must be an integer, not " \
                            f"`{vertex_normal_index_str}`.")
                        return False
                    vertex_normal_index = n
                    # Check if the vertex normal index exists.
                    if vertex_normal_index > 0:
                        if not vertex_normal_index <= num_of_vert_normals:
                            self.logger.log(f"Error in {path}:{index+1}: " \
                                f"Vertex normal with index " \
                                f"{vertex_normal_index} does not exist.")
                            return False
                    elif vertex_normal_index < 0:
                        if not vertex_normal_index >= -num_of_vert_normals:
                            self.logger.log(f"Error in {path}:{index+1}: " \
                                f"Vertex normal with index " \
                                f"{vertex_normal_index} does not exist.")
                            return False
                    else:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            f"Vertex normal with index " \
                            f"{vertex_normal_index} does not exist.")
                        return False
        
        # Check if all faces have the same structure.
        faces_list = []
        for index, line in enumerate(lines):
            line_split = line.split(" ")
            if line_split[0] == "f":
                faces_list.append(line_split[1:])
        
        prev_number_of_slashes = -1
        for face in faces_list:
            for arg in face:
                if not "/" in arg:
                    current_number_of_slashes = 0
                else:
                    current_number_of_slashes = len(arg.split("/")) - 1
                
                if prev_number_of_slashes == -1:
                    prev_number_of_slashes = current_number_of_slashes
                else:
                    if not prev_number_of_slashes == current_number_of_slashes:
                        self.logger.log(f"Error in {path}:{index+1}: " \
                            "Faces must have the same format throughout " \
                            "the file. This is the first occurence where " \
                            "this is not the case.")
                        return False
        
        # Filter the lines list to ommit any lines not containing one of the 
        # following commands: v, vt, vn, f, o. These lines are 
        # kept until this point so the line numbers in the error- and warning-
        # messages are corrected.
        lines_filtered = []
        for index, line in enumerate(lines):
            if line == "":
                continue
            
            if line.startswith("#"):
                continue
            
            line_split = line.split(" ")
            
            if not line_split[0] in ["v", "vt", "vn", "f", "o"]:
                continue
            
            lines_filtered.append(line)
        
        # Return the filtered list of lines of the file.
        return lines_filtered
    
    def get_vertex_and_index_arrays(self, obj_contents):
        """
        The parameter obj_contents should be the variable returned by the 
        get_model_file_contents() function. The function creates lists of 
        vertices, texture coordinates, and vertex normals. Then reads all the 
        faces and creates full vertex data objects from the data fetched from 
        the previously created lists. Then creates numpy arrays from these 
        lists and returns them.
        """
        # Create vertices list, texture coordinates list, vertex normals list,
        # and faces list.
        vertices = []
        texture_coordinates = []
        vertex_normals = []
        faces = []
        
        for line in obj_contents:
            line_split = line.split(" ")
            
            if line_split[0] == "v":
                vertices.append(list(map(float, line_split[1:])))
            elif line_split[0] == "vt":
                texture_coordinates.append(list(map(float, line_split[1:])))
            elif line_split[0] == "vn":
                vertex_normals.append(list(map(float, line_split[1:])))
            elif line_split[0] == "f":
                faces.append(" ".join(line_split[1:]))
            elif line_split[0] == "o":
                self.name = line_split[1]
            else:
                continue
        
        # Create vertex data and index data lists.
        vertex_data = []
        index_data = []
        
        for face in faces:
            for face_element in face.split(" "):
                # Construct vertex attributes list.
                vertex_attributes = []
                #if not "/" in face_element:
                #    vertex_attributes += vertices[int(face_element) - 1]
                
                face_element_split = face_element.split("/")
                vertex_attributes += vertices[int(face_element_split[0]) - 1]
                if len(face_element_split) >= 2:
                    if not face_element_split[1] == "":
                        # Add texture coordinate data.
                        vertex_attributes += texture_coordinates[int(face_element_split[1]) - 1]
                    else:
                        # Add random color data if not texture coordinate data is supplied.
                        vertex_attributes += list(np.random.rand(3))
                #else:
                #    if len(face_element_split) == 1:
                #        vertex_attributes += list(np.random.rand(3))
                if len(face_element_split) >= 3:
                    vertex_attributes += vertex_normals[int(face_element_split[2]) - 1]
                
                index_added = False
                for index, v in enumerate(vertex_data):
                    if v == vertex_attributes:
                        index_data.append(index)
                        index_added = True
                
                if not index_added:
                    vertex_data.append(vertex_attributes)
                    index_data.append(len(vertex_data) - 1)
        
        # Convert vertex data and index data lists to numpy arrays.
        vertex_data_flatten = []
        for v in vertex_data:
            vertex_data_flatten += v
            #vertex_data_flatten += list(np.random.rand(3))
        
        vertex_data = np.array(vertex_data_flatten, dtype=np.float32)
        index_data  = np.array(index_data, dtype=np.uint32)
        
        # Return vertex data and index data numy arrays.
        return vertex_data, index_data
    
    def generate_buffers(self, vertex_data, index_data, texture_data_present, texture_path=""):
        """
        Returns the vao and vbo of this object.
        """
        # Get shader source.
        if texture_data_present:
            with open("src/shaders/model_vertex_shader_texture.glsl", "r") as file:
                vertex_shader_src = file.read()
            with open("src/shaders/model_fragment_shader_texture.glsl", "r") as file:
                fragment_shader_src = file.read()
        else:
            with open("src/shaders/model_vertex_shader_no_texture.glsl", "r") as file:
                vertex_shader_src = file.read()
            with open("src/shaders/model_fragment_shader_no_texture.glsl", "r") as file:
                fragment_shader_src = file.read()
        
        # Compile shaders.
        vertex_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
        
        shader = compileProgram(vertex_shader, fragment_shader)
        
        # Create vbo.
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        # Create ibo.
        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)
        
        # Set a_position attrib array.
        if texture_data_present:
            # vec3 a_position
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
            
            # vec2 a_texture
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
            
            # vec3 a_normal
            #glEnableVertexAttribArray(2)
            #glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
            
            # Generate texture.
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            # Set texture wrapping parameters.
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            # Set texture filtering parameters.
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Load image and store into bound texture.
            image = Image.open(texture_path)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = image.convert("RGBA").tobytes()
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            
            # Unbind texture.
            glBindTexture(GL_TEXTURE_2D, 0)
        else:
            # vec3 a_position
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
            
            # vec3 a_color
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
            
            # vec3 a_normal
            #glEnableVertexAttribArray(2)
            #glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))
        
        # Unbind vbo and ibo buffers.
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        
        # Return shader, vbo, and ibo.
        return shader, vbo, ibo, texture
    
    def render(self, position):
        """
        Binds the vao and vbo of this object and calls opengl drawelements.
        """
        pass
    
    def load_model(self, path):
        """
        Loads vertex attributes into separate arrays, then combines them into 
        a vertex attribute array to store in the GPU. Also loads index/face 
        data.
        """
        # Check if the path exists and if the path is a file.
        if not os.path.exists(path):
            raise Exception(f"File does not exists: {path}")
        if not os.path.isfile(path):
            raise Exception(f"File does not exists: {path}")
        
        # Store file lines into list.
        with open(path, "r") as file:
            lines = file.readlines()
        
        # Remove newlines and leading/trailing spaces. Also ignore commented 
        # lines.
        lines = [line.strip() for line in lines \
            if not line.strip() == "" and not line.strip().startswith("#")]
        
        # Create dictionary to hold matching lines.
        data_dict = {"v": [], "vt": [], "vn": [], "vp": [], "f": []}
        for line in lines:
            line_split = line.split(" ")
            if not line_split[0] in data_dict.keys():
                data_dict[line_split[0]] = []
            data_dict[line_split[0]].append(" ".join(line_split[1:]))
        
        # Create vertex data numpy array.
        valid_attribute_prefixes = ["v", "vt", "vn", "vp"]
        valid_element_prefixes = ["f"]
        
        # Init vertices and indices lists.
        vertices = []
        indices = []
        
        # Loops over all faces.
        for face in data_dict["f"]:
            face = face.strip()
            components = [a for a in face.split(" ") if not a == ""]
            # Loop over all vertices references by the face.
            for component in components:
                # Extract vertex index, texture index, and normal index.
                vertex_index, texture_index, normal_index = component.split("/")
                
                # Convert to special negative one if empty.
                vertex_index = int(vertex_index) if not vertex_index == "" else -1
                texture_index = int(texture_index) if not texture_index == "" else -1
                normal_index = int(normal_index) if not normal_index == "" else -1
                
                # Check index validity.
                if not (vertex_index - 1 < len(data_dict["v"]) and vertex_index > 0):
                    if not vertex_index == -1:
                        self.logger.log(f"Vertex index {vertex_index} does not exist. Skipping face {face}.")
                        continue
                if not (texture_index - 1 < len(data_dict["vt"]) and texture_index > 0):
                    if not texture_index == -1:
                        self.logger.log(f"Texture index {texture_index} does not exist. Skipping face {face}.")
                        continue
                if not (normal_index - 1 < len(data_dict["vn"]) and normal_index > 0):
                    if not normal_index == -1:
                        self.logger.log(f"Normal index {normal_index} does not exist. Skipping face {face}.")
                        continue
                
                # Populate vertices and indices lists.
                # Flag to see if the vertex already exists.
                index_added = False
                # Create new vertex.
                new_vertex = []
                if not len(data_dict["v"]) == 0:
                    tmp_vertex = data_dict["v"][vertex_index-1]
                    tmp_vertex = [a for a in tmp_vertex.strip().split(" ") \
                                    if not a == ""]
                    tmp_vertex = list(map(float, tmp_vertex))
                    new_vertex += tmp_vertex
                if not len(data_dict["vt"]) == 0:
                    tmp_texture = data_dict["vt"][texture_index-1]
                    tmp_texture = [a for a in tmp_texture.strip().split(" ") \
                                    if not a == ""]
                    tmp_texture = list(map(float, tmp_texture))
                    new_vertex += tmp_texture
                if not len(data_dict["vn"]) == 0:
                    tmp_normal = data_dict["vn"][normal_index-1]
                    tmp_normal = [a for a in tmp_normal.strip().split(" ") \
                                    if not a == ""]
                    tmp_normal = list(map(float, tmp_normal))
                    new_vertex += tmp_normal
                # Check if the vertex already exists.
                for index, vertex in enumerate(vertices):
                    # The vertex already exists, add corresponding index.
                    if vertex == new_vertex:
                        indices.append(index)
                        index_added = True
                        break
                
                # Vertex does not exist already, add new vertex and add index.
                if not index_added:
                    vertices.append(new_vertex)
                    indices.append(len(vertices) - 1)
        
        # Flatten vertices array and convert to numpy array.
        vertices_flatten = []
        for vertex in vertices:
            vertices_flatten += vertex
        
        print(vertices_flatten)
        print(indices)

def main():
    logger = lg.Logger()
    
    # Initialize glfw.
    if not glfw.init():
        raise Exception("GLFW could not be initialized.")
    
    # Create window.
    window = glfw.create_window(1920, 1080, "Window Title", None, None)
    
    # Check if the window was created.
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created.")
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_window_pos(window, (3840 - 1920) // 2, (2160 - 1080) // 2)
    
    model = Model(logger)
    obj_contents = model.get_model_file_contents("models/my_quad.obj")
    vertex_data, index_data = model.get_vertex_and_index_arrays(obj_contents)
    shader, vbo, ibo, texture = model.generate_buffers(vertex_data, index_data, True, texture_path="images/test_texture.png")
    
    print(vertex_data)
    print(index_data)
    
    # Opengl stuff.
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glUseProgram(shader)
    
    projection = glGetUniformLocation(shader, "projection")
    translation = glGetUniformLocation(shader, "translation")
    rotation = glGetUniformLocation(shader, "rotation")
    
    ct = 0
    
    while not glfw.window_should_close(window):
        ct = glfw.get_time()
        
        glfw.poll_events()
        
        projection_mat = pyrr.matrix44.create_from_eulers([0, 0, 0])
        translation_mat = pyrr.matrix44.create_from_eulers([0, 0, 0])
        rotation_mat = pyrr.matrix44.create_from_eulers([0, 0, 0])
        
        glUniformMatrix4fv(projection, 1, GL_FALSE, projection_mat)
        glUniformMatrix4fv(translation, 1, GL_FALSE, translation_mat)
        glUniformMatrix4fv(rotation, 1, GL_FALSE, rotation_mat)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        glfw.swap_buffers(window)
    
    # Terminate GLFW.
    glfw.terminate()

if __name__ == "__main__":
    main()