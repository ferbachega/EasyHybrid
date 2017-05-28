#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  representations.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from GLarea.atom_types import get_color
from GLarea.vector_math import Vector


gl_settings = {'sphere_scale':0.15, 'sphere_res':15, 'pretty_res':20, 'selection_radius':1.0, 'ribbon_res':0.4}
select_color = [16, 255, 0, 80]
sel_col_font = [178, 23, 0]
sel_col_font = [178, 0 , 0]

def init_gl(fog_start, fog_end, fovy, width, height, z_near, z_far, color):
    """ Inside the realize function, you should put all you OpenGL
        initialization code, e.g. set the projection matrix,
        the modelview matrix, position of the camera.
    """
    # All OpenGL initialization code goes here
    glMaterialfv(GL_FRONT,GL_AMBIENT, (.7,.7,.7,1.))
    glMaterialfv(GL_FRONT,GL_DIFFUSE, (.8,.8,.8,1.))
    glMaterialfv(GL_FRONT,GL_SPECULAR,(1.,1.,1.,1.))
    glMaterialfv(GL_FRONT,GL_SHININESS,100.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    # FOG
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, fog_start)
    glFogf(GL_FOG_END, fog_end)
    glFogfv(GL_FOG_COLOR, color)
    glFogfv(GL_FOG_DENSITY, 1)
    glEnable(GL_POINT_SMOOTH)
    # light
    light_0_position = [ 1.0,  1.0, 1.0, 0.0]
    light_1_position = [ 1.0, -1.0, 1.0, 0.0]
    light_2_position = [-1.0, -1.0, 1.0, 0.0]
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, light_0_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light_1_position)
    glLightfv(GL_LIGHT2, GL_POSITION, light_2_position)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    #  Antialiased lines
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    # Initialize view
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, float(width)/float(height), z_near, z_far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)


def draw_stick_bond (self, atom1, atom2, radius = 2):
    glMatrixMode(GL_MODELVIEW)
    v = Vector()
    #base of cylinder is at the origin, the top is in the positive z axis
    
    a = atom1.pos
    b = atom2.pos
    
    axis_start = [0, 0, .1]
    #
    axis_end = v.subtract(a, b)

    #find angle between the starting and ending axis
    angle = v.angle(axis_start, axis_end)
    
    # determina the axis of rotation of the angle
    axis_rotation = v.crossproduct (axis_start, axis_end)

    #calculate the distance from a to b

    length = v.mag(axis_end)
    glColor3f(0.9, 0.9, 0.9)

    # set the bottom  and the top radius to be the same thing
    radius_bottom = radius
    radius_top    =  radius

    # draw the bond ( use glTranslate beofre using glRotate)
    cyl = gluNewQuadric()
    glPushMatrix()

    glTranslate(b[0], b[1], b[2])
    #glPushName(0)
    glRotate(angle, axis_rotation[0], axis_rotation[1], axis_rotation[2])
    gluCylinder(cyl, radius_bottom, radius_top, length, 15, 15)
    glPopMatrix()

def draw_bond_line(atom, pos_end):
    """ Draw the bonds.
    """
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    glVertex3f(pos_end[0], pos_end[1], pos_end[2])
    glEnd()
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_dot(atom, point):
    """
    """
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex3f(point[0], point[1], point[2])
    glEnd()
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_point(atom):
    """
    """
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    glEnd()
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_wire_sphere(atom):
    """ Graphs a wired sphere for the given coordinates.
    """
    glMatrixMode(GL_MODELVIEW)
    # Enables the GL_LIGHT0 variable
    glEnable(GL_LIGHT0)
    # Enables lightin three dimensions, i guess
    glEnable(GL_LIGHTING)
    # Enables tha surface colors in 3D, i guess
    glEnable(GL_COLOR_MATERIAL)
    # Enables profundity effect, i guess
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glutWireSphere(atom.radius, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_ball(atom):
    """ Graphs a sphere for the given coordinates.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glutSolidSphere(atom.radius/1.5, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_sphere(atom):
    """ Graphs a sphere for the given coordinates.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glutSolidSphere(atom.cov_rad, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_pretty_vdw(atom):
    """ Graphs a sphere for the given coordinates.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor4ub(atom.col_rgb[0], atom.col_rgb[1], atom.col_rgb[2], 60)
    glutSolidSphere(atom.vdw_rad, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_BLEND)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_vdw(atom):
    """ Graphs a sphere for the given coordinates.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glutSolidSphere(atom.vdw_rad, gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glFlush()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_bond_wired_stick(atom, length, angle, vec_o):
    """ Draw the bonds.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glTranslatef(atom.pos[0], atom.pos[1], atom.pos[2])
    glRotatef(angle, vec_o[0], vec_o[1], vec_o[2])
    glutWireCylinder(0.1, length, 10, 10)
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_ribbon(atom, length, angle, vec_o):
    """ Draw the bonds.
    """
    # The matrix is by default looking at (0,0,1)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glTranslatef(atom.pos[0], atom.pos[1], atom.pos[2])
    glRotatef(angle, vec_o[0], vec_o[1], vec_o[2])
    glutSolidCylinder(gl_settings['ribbon_res'], length, 10, 10)
    glutSolidSphere(gl_settings['ribbon_res'], gl_settings['sphere_res'], gl_settings['sphere_res'])
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_bond_stick(atom, length, angle, vec_o):
    """ Draw the bonds.
    """
    # The matrix is by default looking at (0,0,1)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.index)
    glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glTranslatef(atom.pos[0], atom.pos[1], atom.pos[2])
    glRotatef(angle, vec_o[0], vec_o[1], vec_o[2])
    glutSolidCylinder(0.1, length, 10, 10)
    glPopName()
    glPopMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

def draw_picked(atom, slices=4):
    """ Draw a selection marker to an atom.
    """
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glPushMatrix()
    #glTranslate(atom.pos[0], atom.pos[1], atom.pos[2])
    glPushName(atom.index)
    #glColor4ub(39, 255, 0, 60)
    glColor4ub(select_color[0], select_color[1], select_color[2], select_color[3])
    #glutSolidSphere(0.5, gl_settings['sphere_res'], gl_settings['sphere_res'])
    #glColor3f(atom.color[0], atom.color[1], atom.color[2])
    glPointSize(40)
    glBegin(GL_POINTS)
    glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    glEnd()
    glPopName()
    glPopMatrix()
    glFlush()
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glDisable(GL_BLEND)

def draw_selected(atom, coord):
    """ Draw a selection marker to an atom.
    """
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)
    glPushMatrix()
    glPushName(atom.atom_id)
    glPointSize(20)
    glColor3f(0, 1,1)
    #glColor3ub(0, 100,100)
    glBegin(GL_POINTS)
    glVertex3f(coord[0], coord[1], coord[2])
    glEnd()
    #glPointSize(15)
    #glColor3ub(0, 222, 164)
    #glBegin(GL_POINTS)
    #glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    #glEnd()
    #glPointSize(10)
    #glColor3ub(212, 23, 235)
    #glBegin(GL_POINTS)
    #glVertex3f(atom.pos[0], atom.pos[1], atom.pos[2])
    #glEnd()
    glPopName()
    glPopMatrix()
    glFlush()
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

def draw_numbers(atom, number, coord):
    """ Draw the number of the selected atom.
    """
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_LINE_SMOOTH)
    glColor3f(sel_col_font[0], sel_col_font[1], sel_col_font[2])
    glLineWidth(2)
    glPointSize(2)
    #glTranslate(float(atom.pos[0]), float(atom.pos[1]), float(atom.pos[2]))
    #glScalef(0.006, 0.006, 0.006)
    #glRotate(0, 0, 1, 0)
    #glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(str(number)))
    #glRasterPos2f(float(atom.pos[0]), float( atom.pos[1]))
    glRasterPos3f(float(coord[0]), float(coord[1]), float( coord[2]))
    glutBitmapCharacter( GLUT_BITMAP_HELVETICA_18, ord(str(number)))
    
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

def change_light_properties(gl_ambient=None, gl_diffuse=None, gl_specular=None, gl_position=None):
    """ Function doc
    """
    if gl_ambient is None:
        gl_ambient  = [0.,0.,0.,1.]
    if gl_diffuse is None:
        gl_diffuse  = [1.,1.,1.,1.]
    if gl_specular is None:
        gl_specular = [1.,1.,1.,1.]
    if gl_position is None:
        gl_position = [1.,1.,1.,0.]
    
    glLightfv(GL_LIGHT0,GL_AMBIENT, (gl_ambient[0], gl_ambient[1], gl_ambient[2], gl_ambient[3]))
    
    glLightfv(GL_LIGHT0,GL_DIFFUSE, (gl_diffuse[0], gl_diffuse[1], gl_diffuse[2], gl_diffuse[3]))
    
    glLightfv(GL_LIGHT0,GL_SPECULAR,(gl_specular[0], gl_specular[1], gl_specular[2], gl_specular[3]))
   
    glLightfv(GL_LIGHT0,GL_POSITION,(gl_position[0], gl_position[1], gl_position[2], gl_position[3]))
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, (.7,.7,.7,1.))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (.8,.8,.8,1.))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.,1.,1.,1.))
    glMaterialfv(GL_FRONT, GL_SHININESS, 100.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_FOG)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

def draw_text(text="hola", x=0, y=0):
    """ Function doc
    """
    #glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #gluPerspective(60, 640/480, 0.1, 50)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity( )
    glTranslatef( 0, 0, -4 )
    glDisable( GL_LIGHTING )
    glColor3f( 1, 1, 0.3 )
    glRasterPos3f( 1.8, .5, 0 )
    for c in "tip":
        glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )
    glEnable( GL_LIGHTING )
    glMatrixMode( GL_MODELVIEW )
