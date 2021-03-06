##########################################################################
#  
#  Copyright (c) 2011-2012, John Haddon. All rights reserved.
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

import unittest

import IECore

import Gaffer

class SplinePlugTest( unittest.TestCase ) :

	def testConstructor( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
	
		p = Gaffer.SplineffPlug( "a", defaultValue=s )
		
		self.assertEqual( p.getValue(), s )
		
		s2 = IECore.Splineff(
			IECore.CubicBasisf.linear(),
			(
				( 1, 1 ),
				( 1, 1 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 0, 0 ),
				( 0, 0 ),
			)
		)
		
		p.setValue( s2 )
		
		self.assertEqual( p.getValue(), s2 ) 

	def testSerialisation( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
	
		p = Gaffer.SplineffPlug( "a", defaultValue=s, flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic )
		self.assertEqual( p.getValue(), s )
		
		sn = Gaffer.ScriptNode()
		sn["n"] = Gaffer.Node()
		sn["n"]["p"] = p
		
		se = sn.serialise()
		
		sn = Gaffer.ScriptNode()
		sn.execute( se )
		
		self.assertEqual( sn["n"]["p"].getValue(), s )

	def testPointAccess( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
		p = Gaffer.SplineffPlug( "a", defaultValue=s, flags=Gaffer.Plug.Flags.Dynamic )

		self.assertEqual( p.numPoints(), 6 )
		for i in range( p.numPoints() ) :
			self.assert_( p.pointXPlug( i ).isInstanceOf( Gaffer.FloatPlug.staticTypeId() ) )
			self.assert_( p.pointYPlug( i ).isInstanceOf( Gaffer.FloatPlug.staticTypeId() ) )
			self.assert_( p.pointXPlug( i ).parent().isSame( p.pointPlug( i ) ) )
			self.assert_( p.pointYPlug( i ).parent().isSame( p.pointPlug( i ) ) )

		# accessing nonexistent points should raise exceptions
		self.assertRaises( Exception, p.pointPlug, 6 )
		self.assertRaises( Exception, p.pointXPlug, 6 )
		self.assertRaises( Exception, p.pointYPlug, 6 )

	def testPointDeletion( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
		p = Gaffer.SplineffPlug( "a", defaultValue=s, flags=Gaffer.Plug.Flags.Dynamic )

		self.assertEqual( p.numPoints(), 6 )
		for i in range( p.numPoints() ) :
			self.assert_( p.pointPlug( i ) )
			self.assert_( p.pointXPlug( i ) )
			self.assert_( p.pointYPlug( i ) )
	
		p.removePoint( 0 )

		self.assertEqual( p.numPoints(), 5 )
		for i in range( p.numPoints() ) :
			self.assert_( p.pointPlug( i ) )
			self.assert_( p.pointXPlug( i ) )
			self.assert_( p.pointYPlug( i ) )
				
		p.removeChild( p.pointPlug( 0 ) )
		
		self.assertEqual( p.numPoints(), 4 )
		for i in range( p.numPoints() ) :
			self.assert_( p.pointPlug( i ) )
			self.assert_( p.pointXPlug( i ) )
			self.assert_( p.pointYPlug( i ) )
	
	def testPointTampering( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
		p = Gaffer.SplineffPlug( "a", defaultValue=s, flags=Gaffer.Plug.Flags.Dynamic )
		
		del p.pointPlug( 0 )["x"]
		del p.pointPlug( 0 )["y"]
		
		self.assertRaises( Exception, p.pointXPlug, 0 )
		self.assertRaises( Exception, p.pointYPlug, 0 )
		
	def testPlugSetSignal( self ) :
	
		s = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
		p = Gaffer.SplineffPlug( "a", defaultValue=s, flags=Gaffer.Plug.Flags.Dynamic )
		n = Gaffer.Node()
		n["p"] = p
		
		self.__plugSetCount = 0
		def plugSet( plug ) :
			
			if plug.isSame( p ) :
				self.__plugSetCount += 1
			
		c = n.plugSetSignal().connect( plugSet )
			
		p.pointYPlug( 2 ).setValue( 1.0 )
		
		self.assertEqual( self.__plugSetCount, 1 )
		
		pointIndex = p.addPoint()
		
		self.assertEqual( self.__plugSetCount, 2 )
		 
		p.removePoint( pointIndex )
		
		self.assertEqual( self.__plugSetCount, 3 )		

	def testDefaultValue( self ) :
	
		s1 = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 0, 0 ),
				( 0, 0 ),
				( 0.2, 0.3 ),
				( 0.4, 0.9 ),
				( 1, 1 ),
				( 1, 1 ),
			)
		)
		
		s2 = IECore.Splineff(
			IECore.CubicBasisf.catmullRom(),
			(
				( 1, 1 ),
				( 1, 1 ),
				( 0, 0 ),
				( 0, 0 ),
			)
		)
				
		p = Gaffer.SplineffPlug( "a", defaultValue=s1, flags=Gaffer.Plug.Flags.Dynamic )
		
		self.assertEqual( p.defaultValue(), s1 )
		self.assertEqual( p.getValue(), s1 )
						
		p.setValue( s2 )
		self.assertEqual( p.defaultValue(), s1 )
		self.assertEqual( p.getValue(), s2 )
		
		p.setToDefault()
		self.assertEqual( p.defaultValue(), s1 )
		self.assertEqual( p.getValue(), s1 )
		
if __name__ == "__main__":
	unittest.main()
	
