from openalea.plantik.biotik.growthunit import GrowthUnit 



class testGrowthUnit():

    def __init__(self):
        self.gu = GrowthUnit(min_radius = 0.1)
        assert self.gu.demand == 0
        assert self.gu.resource == 0
        assert self.gu.livingcost == 0

    def test_radius(self):
        assert self.gu.radius == 0.1
        self.gu.radius = 0.2
        assert self.gu.radius == 0.2


    def test_length(self):
        assert self.gu.length == 0
        self.gu.length = 1
        assert self.gu.length == 1

    def test_update(self):
        self.gu.update(1)

    def test_demand(self):
        self.gu.demandCalculation()
    
    def test_resource(self):
        self.gu.resourceCalculation()

    def test_plot(self):
        self.gu.plot(show=False)
