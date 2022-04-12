# Log

## Todo
- [x] Create running opengl window.
- [x] Render 3D objects.
- [ ] View frustrum culling.
- [ ] Lighting.

## 12-04-2022
*20.13-xx.xx*:<br />
- 

## 11-04-2022
*17.40-18.13*:<br />
- Read [learnopengl.org Hello Triangle](https://learnopengl.com/Getting-started/Hello-Triangle) until the VBO section, then switched to [learnopengl.org OpenGL](https://learnopengl.com/Getting-started/OpenGL) to find out what OpenGL objects are.

*18.59-21.35*:<br />
- Finished reading [learnopengl.org OpenGL](https://learnopengl.com/Getting-started/OpenGL).
- Finished reading [learnopengl.org Hello Triangle](https://learnopengl.com/Getting-started/Hello-Triangle) with the result that I now know how to use vao's, vbo's, ibo's, and vertex attribute pointers. I have rendered two triangles with different colors using two different vao's and two different shader programs.

## 10-04-2022
*14.10-18.00*:<br />
- Finished the function `get_model_file_contents()`, which has the function of validating the entire obj file and return false if any errors are encountered due to which the file would be unusable. The function is really long (341 lines), I also didn't write tests for this function, because it would take far too long and would demotivate me to continue. I might write tests in the future, but getting this done was extremely important today. I might be able to format the data correctly and render the first model tonight.

*19.33-21.51*:<br />
- Created and finished function `get_vertex_and_index_arrays()`, which converts the obj_contents returned from the `get_model_file_contents()` function into a vertex data numpy array and an index data numpy array.
- Integrated the glfw window into `model.py`, got a quad to render, but cant get it to have color.
- I can't get it to work properly, I should just remove color from the shader if no texture is provided, I think it will be rendered as white, it can get shaded later when I add lighting. I should look up what the default steps are for storing model data and texture data, and for rendering a model.

## 09-04-2022
*11.53-13.06*:<br />
- Started implementing a validator function for the file contents of obj files.
- Closed a bunch of tabs to free 3 GB of memory.
- Finished verification of vertex attributes in obj files. Next, I should research the obj format, because appearantly there are groups as well.

## 07-04-2022
*10.57-12.40*:<br />
- Watched videos on vao's and vbo's.
- Created a new window using GLFW instead of GLUT.
- Created simple logger class.
- Drawn a triangle using a buffer object and shaders in the programmable pipeline.

*15.25-16.28*:<br />
- Rendered a rotating 3D cube using [atibyte's tutorial](https://www.youtube.com/watch?v=YP3oibttzh4&list=PL1P11yPQAo7opIg8r-4BMfh1Z_dCOfI0y&index=6).
- Committed changes to remote repository.
- Created and switched to branch `development`.
- Started on the [textured cube tutorial by atibyte](https://www.youtube.com/watch?v=0kPxilkCX_c&list=PL1P11yPQAo7opIg8r-4BMfh1Z_dCOfI0y&index=7).

*20.07-21.45*:
- Rendered a textured cube.
- Started implementing the Model class.

*23.08-23.46*:
- Added .obj interpreter until a list of vertex data and a list of index data. The lists just need to be converted to numpy arrays and the stride and offset needs to be calculated.

## 06-04-2022
*20.08-21.18*<br />
- Created repository.
- Created a running GLUT OpenGL window. It didn't work at first because glutInit() raised a NullPointerException, fixed it using [this](https://stackoverflow.com/questions/65699670/pyopengl-opengl-error-nullfunctionerror-attempt-to-call-an-undefined-functio) stack overflow question. It still threw a warning about `CreateDC`, which I fixed by adding `del os.environ['DISPLAY']` at the start following [this](https://stackoverflow.com/questions/65347825/createdc-failed-screen-size-info-may-be-incorrect) stack overflow question.
- Drawn a pink square on the screen.