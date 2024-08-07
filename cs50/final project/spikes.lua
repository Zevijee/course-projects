local player = require 'player'

local spike = {}
spike.__index = spike
local activate_spikes = {}

function spike.new(x, y, damage, respawn, respawnX, respawnY)
    -- setting a new spike instance
    local i = setmetatable({}, spike)

    i.damage = damage

    -- dims
    i.x = x
    i.y = y
    i.img = love.graphics.newImage('assets/gfx/spikes.png')
    i.w = i.img:getWidth()
    i.h = i.img:getHeight()
    i.respawn = respawn
    i.respawnX = respawnX
    i.respawnY = respawnY
    
    -- physics
    i.p = {}
    i.p.body = love.physics.newBody(world, i.x, i.y, 'static')
    i.p.shape = love.physics.newRectangleShape(i.w, i.h)
    i.p.fixture = love.physics.newFixture(i.p.body, i.p.shape)
    -- i.p.fixture:setSensor(true)
    
    table.insert(activate_spikes, i)
end

-- updates each spike
function spike:update(dt)

end

-- gets each spike to update
function spike.update_all(dt)
    for i,instance in ipairs(activate_spikes) do
        instance:update(dt)
    end
end

-- handles collisions
function spike.beginContact(a, b, collision)
    for i,instance in ipairs(activate_spikes) do
        if a == instance.p.fixture or b == instance.p.fixture then
            if a == player.p.fixture or b == player.p.fixture then
                player:takeDamage(instance.damage, instance.respawn, instance.respawnX, instance.respawnY)
                return true
            end
        end
    end
end

-- draws each spike
function spike:draw()
    love.graphics.draw(self.img, self.x, self.y, 0, 2, 2, self.w/2, self.h/2)
    -- love.graphics.polygon("line", self.p.body:getWorldPoints(self.p.shape:getPoints()))
end

-- gets each spike to be drawn
function spike.draw_all()
    for i,instance in ipairs(activate_spikes) do
        instance:draw()
    end
end

-- removes all the spikes
function spike:remove_all()
    for i,v in ipairs(activate_spikes) do
        v.p.body:destroy()
    end

    activate_spikes = {}
end


return spike
