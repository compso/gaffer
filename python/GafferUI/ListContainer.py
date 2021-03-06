##########################################################################
#  
#  Copyright (c) 2011, John Haddon. All rights reserved.
#  Copyright (c) 2011-2012, Image Engine Design Inc. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

from IECore import Enum

import GafferUI

QtGui = GafferUI._qtImport( "QtGui" )

## The ListContainer holds a series of Widgets either in a column or a row.
# It attempts to provide a list like interface for manipulation of the widgets.
class ListContainer( GafferUI.ContainerWidget ) :

	Orientation = Enum.create( "Vertical", "Horizontal" )

	def __init__( self, orientation=Orientation.Vertical, spacing=0, borderWidth=0, **kw ) :
	
		GafferUI.ContainerWidget.__init__( self, QtGui.QWidget(), **kw )
	
		if orientation==self.Orientation.Vertical :
			self.__qtLayout = QtGui.QVBoxLayout()
		else :
			self.__qtLayout = QtGui.QHBoxLayout()
	
		self.__qtLayout.setSpacing( spacing )
		self.__qtLayout.setContentsMargins( borderWidth, borderWidth, borderWidth, borderWidth )
		self.__qtLayout.setSizeConstraint( QtGui.QLayout.SetMinAndMaxSize )
	
		self._qtWidget().setLayout( self.__qtLayout )
	
		self.__orientation = orientation
		self.__widgets = []
	
	def orientation( self ) :
	
		return self.__orientation
		
	def append( self, child, expand=False ) :
		
		assert( isinstance( child, GafferUI.Widget ) )

		oldParent = child.parent()
		if oldParent is not None :
			oldParent.removeChild( child )
	
		self.__widgets.append( child )
		
		stretch = 1 if expand else 0
		self.__qtLayout.addWidget( child._qtWidget(), stretch )	
		child._applyVisibility()
	
	def remove( self, child ) :
	
		self.removeChild( child )
	
	def insert( self, index, child, expand=False ) :
	
		l = len( self.__widgets )
		if index > l :
			index = l
	
		oldParent = child.parent()
		if oldParent is not None :
			oldParent.removeChild( child )
			
		self.__widgets.insert( index, child )

		stretch = 1 if expand else 0
		self.__qtLayout.insertWidget( index, child._qtWidget(), stretch )
		child._applyVisibility()
		
	def index( self, child ) :
	
		return self.__widgets.index( child )
	
	def __setitem__( self, index, child ) :
	
		if isinstance( index, slice ) :
			assert( isinstance( child, list ) )
			children = child
			insertionIndex = index.start if index.start is not None else 0
		else :
			children = [ child ]
			insertionIndex = index
			
		expands = []
		for i in range( insertionIndex, insertionIndex + len( children ) ) :
			if i < len( self ) :
				expands.append( self.__qtLayout.stretch( i ) > 0 )
			else :
				expands.append( False )

		del self[index]
		
		for i in range( len( children ) - 1, -1, -1 ) :
			self.insert( insertionIndex, children[i], expands[i] )
	
	def __getitem__( self, index ) :
	
		return self.__widgets[index]
		
	def __delitem__( self, index ) :
		
		if isinstance( index, slice ) :
			indices = range( *(index.indices( len( self ) )) )
			for i in indices :
				self[i]._qtWidget().setParent( None )
				self[i]._applyVisibility()
			del self.__widgets[index]
		else :
			self.__widgets[index]._qtWidget().setParent( None )
			self.__widgets[index]._applyVisibility()
			del self.__widgets[index]

	def __len__( self ) :
	
		return len( self.__widgets )
	
	def addChild( self, child, expand=False ) :
	
		self.append( child, expand )
	
	def removeChild( self, child ) :
	
		self.__widgets.remove( child )
		child._qtWidget().setParent( None )
		child._applyVisibility()
		
	def setExpand( self, child, expand ) :
	
		self.__qtLayout.setStretchFactor( child._qtWidget(), 1 if expand else 0 )
	
	def getExpand( self, child ) :
	
		stretch = self.__qtLayout.stretch( self.index( child ) )
		return stretch > 0
		