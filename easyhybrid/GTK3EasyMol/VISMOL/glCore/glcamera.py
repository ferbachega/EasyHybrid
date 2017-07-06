#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  glcamera.py
#  
#  Copyright 2016 Labio <labio@labio-XPS-8300>
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

import math
import numpy as np
import VISMOL.glCore.matrix_operations as mop
import VISMOL.glCore.operations as op

class GLCamera():
    """ Class doc
    """
    
    def __init__ (self, fov=30.0, z_n=0.01, z_f=10.0, var=(4.0/3.0), pos=np.array([0,0,3],dtype=np.float32), fog_s=8.0, fog_e=10.0):
        """ Class initialiser
        """
        self.field_of_view = fov
        self.z_near = z_n
        self.z_far = z_f
        self.viewport_aspect_ratio = var
        self.position = pos
        self.fog_start = fog_s
        self.fog_end = fog_e
        self.max_vertical_angle = 85.0  # must be less than 90 to avoid gimbal lock
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0
        self.view_matrix = self._get_view_matrix()
        self.projection_matrix = self._get_projection_matrix()
    
    def get_position(self):
        """ Returns the x, y, z position of the camera in 
            absolute coordinates.
        """
        return self.position
    
    def set_position(self, new_position):
        """ Function doc
        """
        new_position = np.array(new_position,dtype=np.float32)
        assert(new_position.size==3)
        self.position = new_position
        return True
    
    def move_position(self, new_position):
        """ Function doc
        """
        new_position = np.array(new_position,dtype=np.float32)
        assert(new_position.size==3)
        self.position += new_position
        return True
    
    def get_field_of_view(self):
        """ Function doc
        """
        return self.field_of_view
    
    def set_field_of_view(self, new_fov):
        """ Function doc
        """
        assert(new_fov>0.0 and new_fov<180.0)
        self.field_of_view = new_fov
        return True
    
    def set_znear_zfar(self, new_znear, new_zfar):
        """ Function doc
        """
        assert(new_znear>0.0)
        assert(new_znear<new_zfar)
        self.z_near = new_znear
        self.z_far = new_zfar
        return True
    
    def get_orientation(self):
        """ Function doc
        """
        orientation_matrix = mop.my_glRotatef(np.identity(4,dtype=np.float32),
                                              self.vertical_angle,[1,0,0])
        orientation_matrix = mop.my_glRotatef(orientation_matrix,
                                              self.horizontal_angle,[0,1,0])
        return orientation_matrix
    
    def _normalize_angles(self):
        """ Function doc
        """
        self.horizontal_angle = self.horizontal_angle % 360.0
        if self.horizontal_angle<0:
            self.horizontal_angle += 360.0
        if self.vertical_angle>self.max_vertical_angle:
            self.vertical_angle = self.max_vertical_angle
        elif self.vertical_angle<-self.max_vertical_angle:
            self.vertical_angle = -self.max_vertical_angle
    
    def add_orientation_angles(self, h_angle, v_angle):
        """ Function doc
        """
        self.horizontal_angle += h_angle
        self.vertical_angle += v_angle
        self._normalize_angles()
        return True
    
    def look_at(self, target):
        """ Function doc
        """
        assert(self.position[0]!=target[0] and
               self.position[1]!=target[1] and
               self.position[2]!=target[2])
        direction = op.unit_vector(target-self.position)
        self.vertical_angle = -math.asin(direction[1])*180/math.pi
        self.horizontal_angle = -(math.atan2(-direction[0],-direction[2])*180/math.pi)
        self._normalize_angles()
        return True
    
    def set_viewport_aspect_ratio(self, new_var):
        """ Function doc
        """
        assert(new_var>0.0)
        self.viewport_aspect_ratio = new_var
        return True
    
    def get_matrix(self):
        """ Function doc
        """
        return mop.my_glMultiplyMatricesf(self.get_projection_matrix(),
                                          self.get_view_matrix())
    
    def _get_projection_matrix(self):
        """ Function doc
        """
        assert(self.field_of_view>0.0 and self.field_of_view<180.0)
        assert(self.z_near>0.0)
        assert(self.z_near<self.z_far)
        assert(self.viewport_aspect_ratio>0.0)
        return mop.my_glPerspectivef(self.field_of_view,self.viewport_aspect_ratio,self.z_near,self.z_far)
    
    def _get_view_matrix(self):
        """ Function doc
        """
        trans = mop.my_glTranslatef(np.identity(4,dtype=np.float32),-self.position)
        orient = self.get_orientation()
        view = mop.my_glMultiplyMatricesf(trans, orient)
        return view
    
    def set_view_matrix(self, new_view_matrix):
        """ Function doc
        """
        self.view_matrix = new_view_matrix
    
    def set_projection_matrix(self, new_proj_matrix):
        """ Function doc
        """
        self.projection_matrix = new_proj_matrix
    
