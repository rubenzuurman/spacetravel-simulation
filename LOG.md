# Log

## Todo
- [x] Create running opengl window.
- [ ] Render 3D objects.
- [ ] View frustrum culling.
- [ ] Lighting.

## 06-04-2022
*20.08-21.18*<br />
- Created repository.
- Created a running GLUT OpenGL window. It didn't work at first because glutInit() raised a NullPointerException, fixed it using [this](https://stackoverflow.com/questions/65699670/pyopengl-opengl-error-nullfunctionerror-attempt-to-call-an-undefined-functio) stack overflow question. It still threw a warning about `CreateDC`, which I fixed by adding `del os.environ['DISPLAY']` at the start following [this](https://stackoverflow.com/questions/65347825/createdc-failed-screen-size-info-may-be-incorrect) stack overflow question.
- Drawn a pink square on the screen.