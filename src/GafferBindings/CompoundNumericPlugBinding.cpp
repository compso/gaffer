//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2011-2012, John Haddon. All rights reserved.
//  Copyright (c) 2011-2013, Image Engine Design Inc. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#include "boost/python.hpp"

#include "IECorePython/IECoreBinding.h"
#include "IECorePython/RunTimeTypedBinding.h"

#include "Gaffer/CompoundNumericPlug.h"

#include "GafferBindings/CompoundNumericPlugBinding.h"
#include "GafferBindings/PlugBinding.h"

using namespace boost::python;
using namespace GafferBindings;
using namespace Gaffer;

template<typename T>
static std::string compoundNumericPlugRepr( const T *plug )
{
	std::string result = Serialisation::classPath( plug ) + "( \"" + plug->getName().string() + "\", ";
	
	if( plug->direction()!=Plug::In )
	{
		result += "direction = " + PlugSerialiser::directionRepr( plug->direction() ) + ", ";
	}
		
	typename T::ValueType v;
	if( plug->defaultValue()!=typename T::ValueType( 0 ) )
	{
		v = plug->defaultValue();
		result += "defaultValue = " + IECorePython::repr( v ) + ", ";
	}
	
	if( plug->hasMinValue() )
	{
		v = plug->minValue();
		result += "minValue = " + IECorePython::repr( v ) + ", ";
	}
	
	if( plug->hasMaxValue() )
	{
		v = plug->maxValue();
		result += "maxValue = " + IECorePython::repr( v ) + ", ";
	}
	
	if( plug->getFlags() != Plug::Default )
	{
		result += "flags = " + PlugSerialiser::flagsRepr( plug->getFlags() ) + ", ";
	}
	
	result += ")";

	return result;
}

template<typename T>
static void bind()
{
	typedef typename T::ValueType V;
		
	IECorePython::RunTimeTypedClass<T>()
		.def( init<const char *, Plug::Direction, V, V, V, unsigned>(
				(
					boost::python::arg_( "name" )=GraphComponent::defaultName<T>(),
					boost::python::arg_( "direction" )=Plug::In,
					boost::python::arg_( "defaultValue" )=V( 0 ),
					boost::python::arg_( "minValue" )=V(Imath::limits<typename V::BaseType>::min()),
					boost::python::arg_( "maxValue" )=V(Imath::limits<typename V::BaseType>::max()),
					boost::python::arg_( "flags" )=Plug::Default
				)
			)
		)
		.GAFFERBINDINGS_DEFPLUGWRAPPERFNS( T )
		.def( "defaultValue", &T::defaultValue )
		.def( "hasMinValue", &T::hasMinValue )
		.def( "hasMaxValue", &T::hasMaxValue )
		.def( "minValue", &T::minValue )
		.def( "maxValue", &T::maxValue )
		.def( "setValue", &T::setValue )
		.def( "getValue", &T::getValue )
		.def( "__repr__", &compoundNumericPlugRepr<T> )
	;

}

void GafferBindings::bindCompoundNumericPlug()
{
	bind<V2fPlug>();
	bind<V3fPlug>();
	bind<V2iPlug>();
	bind<V3iPlug>();
	bind<Color3fPlug>();
	bind<Color4fPlug>();
}
