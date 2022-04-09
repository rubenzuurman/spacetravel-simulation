# Log

## Todo
- [x] Create running opengl window.
- [ ] Render 3D objects.
- [ ] View frustrum culling.
- [ ] Lighting.

## 07-04-2022
*10.57-12.40*:<br />
- Watched videos on vao's and vbo's.
- Created a new window using GLFW instead of GLUT.
- Created simple logger class.
- Drawn a triangle using a buffer object and shaders in the programmable pipeline.

*15.25-xx.xx*:<br />
- Rendered a rotating 3D cube using [atibyte's tutorial](https://www.youtube.com/watch?v=YP3oibttzh4&list=PL1P11yPQAo7opIg8r-4BMfh1Z_dCOfI0y&index=6).

## 06-04-2022
*20.08-21.18*<br />
- Created repository.
- Created a running GLUT OpenGL window. It didn't work at first because glutInit() raised a NullPointerException, fixed it using [this](https://stackoverflow.com/questions/65699670/pyopengl-opengl-error-nullfunctionerror-attempt-to-call-an-undefined-functio) stack overflow question. It still threw a warning about `CreateDC`, which I fixed by adding `del os.environ['DISPLAY']` at the start following [this](https://stackoverflow.com/questions/65347825/createdc-failed-screen-size-info-may-be-incorrect) stack overflow question.
- Drawn a pink square on the screen.