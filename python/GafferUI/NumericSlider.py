##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
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

import math

import IECore

import GafferUI

QtGui = GafferUI._qtImport( "QtGui" )

## The NumericSlider extends the slider class to provide a mapping between the position
# and a range defined by a minimum and maximum value.
class NumericSlider( GafferUI.Slider ) :

	## The type of value (int or float) determines the type of the slider.
	# The min and max arguments define the numeric values at the ends of the slider.
	# By default, values outside this range will be clamped, but hardMin and hardMax
	# may be specified to move the point at which the clamping happens outside of the
	# slider itself.
	def __init__( self, value=0, min=0, max=1, hardMin=None, hardMax=None, **kw ) :
	
		GafferUI.Slider.__init__( self, **kw )
		
		self.__min = min
		self.__max = max
		self.__hardMin = hardMin if hardMin is not None else self.__min
		self.__hardMax = hardMax if hardMax is not None else self.__max
		
		# It would be nice to not store value, but always infer it from position.
		# This isn't possible though, as the range may be 0 length and then we
		# would lose the value.
		self.__value = value
		
		self.__setPosition()
	
	def setPosition( self, position ) :
		
		# change it into a setValue call so we can apply clamping etc.
		self.setValue( self.__min + position * ( self.__max - self.__min ) )
	
	def setValue( self, value ) :
		
		value = max( self.__hardMin, min( self.__hardMax, value ) )
		
		if value == self.__value :
			return

		self.__value = value
		self.__setPosition()
		
		try :
			signal = self.__valueChangedSignal
		except :
			return
		
		signal( self )
			
	def getValue( self ) :
	
		return self.__value
		
	def setRange( self, min, max, hardMin=None, hardMax=None ) :
	
		if hardMin is None :
			hardMin = min
		if hardMax is None :
			hardMax = max
	
		if min==self.__min and max==self.__max and hardMin==self.__hardMin and hardMax==self.__hardMax :
			return
	
		self.__min = min
		self.__max = max
		self.__hardMin = hardMin
		self.__hardMax = hardMax
		
		self.setValue( self.__value ) # reclamps the value to the range if necessary
		self.__setPosition() # updates the position in the case that setValue() didn't
		# __setPosition() won't trigger an update if the position is the same - if
		# the position is at one end of the range, and that end is the same as before.
		self._qtWidget().update()
		
	def getRange( self ) :
	
		return self.__min, self.__max, self.__hardMin, self.__hardMax
		
	def valueChangedSignal( self ) :
	
		try :
			return self.__valueChangedSignal
		except :
			self.__valueChangedSignal = GafferUI.WidgetSignal()
			
		return self.__valueChangedSignal
	
	def __setPosition( self ) :
	
		range = self.__max - self.__min
		if range == 0 :
			GafferUI.Slider.setPosition( self, 0 )
		else :
			GafferUI.Slider.setPosition( self, float(self.__value - self.__min) / range )		
	
  	def _drawBackground( self, painter ) :
  		  		
  		size = self.size()
   		valueRange = self.__max - self.__min
   		if valueRange == 0 :
   			return
   		
   		idealSpacing = 10
		idealNumTicks = float( size.x ) / idealSpacing
		tickStep = valueRange / idealNumTicks
		
		logTickStep = math.log10( tickStep )
		flooredLogTickStep = math.floor( logTickStep )
		tickStep = math.pow( 10, flooredLogTickStep )
		blend = (logTickStep - flooredLogTickStep)
	
		tickValue = math.floor( self.__min / tickStep ) * tickStep
		i = 0
		while tickValue <= self.__max :
			x = size.x * ( tickValue - self.__min ) / valueRange
			if i % 100 == 0 :
				height0 = height1 = 0.75
				alpha0 = alpha1 = 1
			elif i % 50 == 0 :
				height0 = 0.75
				height1 = 0.5
				alpha0 = alpha1 = 1
			elif i % 10 == 0 :
				height0 = 0.75
				height1 = 0.25
				alpha0 = alpha1 = 1
			elif i % 5 == 0 :
				height0 = 0.5
				height1 = 0
				alpha0 = 1
				alpha1 = 0
			else :
				height0 = 0.25
				height1 = 0
				alpha0 = 1
				alpha1 = 0
			
			alpha = alpha0 + (alpha1 - alpha0) * blend			
			height = height0 + (height1 - height0) * blend
			
			pen = QtGui.QPen()
			pen.setWidth( 0 )
			pen.setColor( QtGui.QColor( 0, 0, 0, alpha * 255 ) )
			painter.setPen( pen )
			
			painter.drawLine( x, size.y, x, size.y * ( 1 - height ) )
			tickValue += tickStep
			i += 1		
