#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Branch module

.. module branch
    :synopsis: Branches utilities and classes

.. topic:: summary

    Branches utilities and classes

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $
    :Usage:
        >>> from openalea.plantik.biotik.branch import *

.. testsetup::

    from openalea.plantik.biotik.branch import *

"""
from openalea.plantik.biotik.component import *
from openalea.plantik.biotik.collection import CollectionVariables, SingleVariable
from openalea.plantik.biotik.context import Context



class Branch(ComponentInterface):
    """Branch class

    Specialised version of :class:`~openalea.plantik.biotik.component.ComponentInterface`
    dedicated to Branches.

    Branch class does not compute anything special, it mainly serves as storage for various
    information. The update of the length and radius is made in the :mod:`plants` module.

    .. warning:: 

        If the parameter store_data is True, then the :attr:`variables` attributes will store 
        the length, radius and age at each time step, which may be costly. Consider to set it to False
        if required.

    :Example:

    >>> from openalea.plantik.biotik.branch import *
    >>> branch = Branch()
    >>> branch.radius
    0.001
    >>> branch.variables.radius.values
    [0.001]


    :plotting:

    If the store_data is True, the you can plot results either from the class instance :meth:`plot`
    of from the variables stored in :attr:`variables`. The former being less flexible with only `plot` of
    radius versus age, length versus age, length versus radius. And the latter provides plot of variable
    versus age (the same as before) as well as histograms.



    """
    def __init__(self, birthdate=None, id=None, min_radius=0.001,
                 order=0, path=1, rank=1, store_data=True):
        """**Constructor**

        :param datetime.datetime birthdate: 
        :param int id:  
        :param float min_radius: in meters 
        :param int order: 
        :param int path: 
        :param int rank: 
        :param int store_data: 

        :attributes:
            * :attr:`length`: total length of the branch in meters
            * :attr:`radius`:  radius of at the base of the branch (see plants module)
            * those inherited by :class:`~openalea.plantik.biotik.component.ComponentInterface`: 
              :attr:`age`, :attr:`demand`, :attr:`birthdate`, ...
            * :attr:`internode_counter`  count number of internodes in this branch
            * :attr:`growthunit_counter` count number of growth units in this branch
            * :attr:`variables` is a :class:`CollectionVariables` instance containing the :attr:`age`, 
              :attr:`radius` and :attr:`length` at each time step
        """
        self.context = Context(rank=rank, order=order, path=path)
        ComponentInterface.__init__(self, label='Branch', birthdate=birthdate, id=id)

        self.store_data = store_data
        self._length = 0.
        self._radius = min_radius

        self.variables = CollectionVariables()
        self.variables.add(SingleVariable(name='age', unit='days', values=[self.age.days]))
        self.variables.add(SingleVariable(name='length', unit='meters', values=[self.length]))
        self.variables.add(SingleVariable(name='radius', unit='meters', values=[self.radius]))


        self.internode_counter = 0. # count number of internodes in this branch
        self.growthunit_counter = 0.# count number of growth units in this branch

    def _getRadius(self):
        return self._radius
    def _setRadius(self, value):
        if value< self._radius:
            print "radius decreased in branch update!!"
        self._radius = value
    radius = property(_getRadius, _setRadius, None, "getter/setter to the branch radius")

    def _getLength(self):
        return self._length
    def _setLength(self, value):
        self._length = value
    length = property(_getLength, _setLength, None, "getter/setter to the branch length")

    def update(self, dt):
        """Update the branch characteristics at each time step


        Update the :attr:`age` of the component by **dt**
        if **store_data** is True, it also append the age,
        length and radius to :attr:`variables`

        :param float,int,datetime.timedelta dt: in days
        """
        super(Branch, self).update(dt)
        if self.store_data is True:
            self.variables.age.append(self.age.days)
            self.variables.length.append(self.length)
            self.variables.radius.append(self.radius)


    def demandCalculation(self, **kargs):
        """no demand for a branch (i.e., zero)"""
        pass

    def resourceCalculation(self, **kargs):
        """no resource for a branch (i.e., zero)"""
        pass

    def plot(self, variables=['length', 'radius'], show=True, **args):
        """plot some results

        :param list variables: plot results related to the variables provided
        :param bool show: create but do not show the plot (useful for test, saving)
        :param  args: any parameters that pylab.plot would accept.

        .. plot::
            :width: 50%
            :include-source:

            from openalea.plantik.biotik.branch import *
            b = Branch()
            for v in range(1,100):
                b.radius = (v*0.001)**0.5
                b.length = v*0.01
                b.update(1)
            b.plot(variables=['radius'])

        """
        self.variables.valid_names(variables)
        import pylab
        #_variables = checkVariables(self.variables, variables)

        count = 1
        if 'length' in variables:
            pylab.figure(count)
            self.variables.length.plot(show=show, **args)
            count += 1

        if 'radius' in variables:
            pylab.figure(count)
            self.variables.radius.plot(show=show, **args)
            count += 1

        pylab.figure(count)
        length = self.variables.length
        radius = self.variables.radius
        pylab.plot(length.values, radius.values, 'o-')
        pylab.xlabel('Length (%s)' % length.unit)
        pylab.ylabel('Radius (%s)' % radius.unit)
        pylab.grid(True)
        if show == True:
            pylab.show()

