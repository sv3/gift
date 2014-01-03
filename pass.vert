varying vec2 uv;
 
void
main() {
  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
  uv = vec2(gl_MultiTexCoord0);
}
