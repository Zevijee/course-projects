local player = require 'player'

local coin = {}
coin.__index = coin
local activate_coins = {}

function coin.new(x, y)
    -- setting a new coin instance
    local i = setmetatable({}, coin)

    -- dims
    i.x = x
    i.y = y
    i.img = love.graphics.newImage('assets/gfx/coin.png')
    i.w = i.img:getWidth()
    i.h = i.img:getHeight()

    -- for spinning
    i.scaleX = 1
    i.random_time_offset = math.random(0, 100)

    -- for collisions
    i.b_removed = false
    
    -- physics
    i.p = {}
    i.p.body = love.physics.newBody(world, i.x, i.y, 'static')
    i.p.shape = love.physics.newRectangleShape(i.w, i.h)
    i.p.fixture = love.physics.newFixture(i.p.body, i.p.shape)
    i.p.fixture:setSensor(true)
    
    table.insert(activate_coins, i)
end

-- updates each coin
function coin:update(dt)
    self:spin(dt)
    self:check_removed()
end

-- gets each coin to update
function coin.update_all(dt)
    for i,instance in ipairs(activate_coins) do
        instance:update(dt)
    end
end

-- spins the coins
function coin:spin(dt)
    self.scaleX = math.sin(love.timer.getTime() * 2 + self.random_time_offset)
end

-- removes coins that need to be removed
function coin:remove()
    for i, instance in ipairs(activate_coins) do
        if instance == self then
            self.p.body:destroy()
            table.remove(activate_coins, i)
            player:increment_coins(1)
        end
    end
end

-- checks if coins need to be removed
function coin:check_removed()
    if self.b_removed then
        self:remove()
    end
end

-- makes the coins spin
function coin:spin(dt)
    self.scaleX = math.sin(love.timer.getTime() * 2 + self.random_time_offset)
end

-- handles collisions
function coin.beginContact(a, b, collision)
    for i,instance in ipairs(activate_coins) do
        if a == instance.p.fixture or b == instance.p.fixture then
            if a == player.p.fixture or b == player.p.fixture then
                instance.b_removed = true
                coinCollect = true
                return true
            end
        end
    end
end

-- draws each coin
function coin:draw()
    love.graphics.draw(self.img, self.x, self.y, 0, 2 * self.scaleX, 2, self.w/2, self.h/2)
    -- love.graphics.polygon("line", self.p.body:getWorldPoints(self.p.shape:getPoints()))
end

-- gets each coin to be drawn
function coin.draw_all()
    for i,instance in ipairs(activate_coins) do
        instance:draw()
    end
end

-- removes all the coins
function coin:remove_all()
    for i,v in ipairs(activate_coins) do
        v.p.body:destroy()
    end

    activate_coins = {}
end

return coin
