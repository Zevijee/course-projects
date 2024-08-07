local player = require 'player'

local boss = {}
boss.__index = boss
local activate_bosss = {}

boss.number = 0
boss.health = 10

function boss.new(x, y, damage, rage, scaleX, scaleY)
    -- setting a new boss instance
    local i = setmetatable({}, boss)
    i:loadAssets()

    i.hit = love.audio.newSource('assets/sfx/hit.wav', 'static')

    i.damage = damage or 1

    -- dims and movement
    i.x = x
    i.y = y
    i.scaleX = 1
    i.offset_y = 8
    i.speedmod = 3
    i.xVel = 80
    i.xVelTimer = 0

    -- to scale bigger
    i.scale = {}
    i.scale.x = scaleX
    i.scale.y = scaleY

    -- for the rage
    i.rage = rage

    -- anims
    i.animation = {timer = 0, rate = 0.1}
    i.animation.run = {total = 4, current = 1, img = i.runAnim}
    i.animation.walk = {total = 4, current = 1, img = i.walkAnim}
    i.animation.draw = i.animation.walk.img[1]
    
    -- physics
    i.p = {}
    i.p.body = love.physics.newBody(world, i.x, i.y, 'dynamic')
    i.p.body:setFixedRotation(true)
    i.p.shape = love.physics.newRectangleShape(i.w * 0.4, i.h * 0.75)
    i.p.fixture = love.physics.newFixture(i.p.body, i.p.shape)
    i.p.body:setMass(75)
    -- i.p.fixture:setSensor(true)
    
    -- for the bosss health and if hurt
    boss.health = 10
    i.hurtBool = false
    i.hurtCounter = 0
    i.turnRed = false
    i.first = true
    i.died = false
    i.withinAttackRangeBool = false
    
    table.insert(activate_bosss, i)

    if i.rage then
        i.state = i.animation.run
    else
        i.state = i.animation.walk
    end
end

function boss:loadAssets()
    boss.runAnim = {}
    for i=1, 4 do
        boss.runAnim[i] = love.graphics.newImage('assets/gfx/enemy/run/' ..i.. '.png')
    end

    boss.walkAnim = {}
    for i=1, 4 do
        boss.walkAnim[i] = love.graphics.newImage('assets/gfx/enemy/walk/' ..i.. '.png')
    end

    boss.w = boss.walkAnim[1]:getWidth() * 5
    boss.h = boss.walkAnim[1]:getHeight() * 3.5
end

-- updates each boss
function boss:update(dt)
    self:syncPhysics()
    self:animate(dt)
    self:attacked()
    self:hurt()
    self:die()
    self:withinAttackRange()

    boss.currentHealth = self.currentHealth
end

-- checks if boss is within the attack range of the player
function boss:withinAttackRange()
    -- print(self.currentHealth)
    local distanceToPlayerX = math.abs(self.x - player.d.x)
    local distanceToPlayerY = math.abs(self.y - player.d.y)
    if distanceToPlayerX <= 200 and distanceToPlayerY <= 100 then
        self.withinAttackRangeBool = true
    else
        self.withinAttackRangeBool = false
    end
end

-- kills the boss
function boss:kill()
    for i, instance in ipairs(activate_bosss) do
        if instance == self then
            self.p.body:destroy()
            table.remove(activate_bosss, i)
            player:increment_coins(100000)
            boss.number = 1
        end
    end
end

-- checks if the player died 
function boss:die()
    if boss.health <= 0 then
        self:kill()
    end
end

-- makes a boss hurt anim
function boss:hurt()
    if self.hurt and self.hurtCounter > 500 then
        self.hurtBool = false
        self.hurtCounter = 0
        self.first = true
    elseif self.hurt then
        self.hurtCounter  = self.hurtCounter + 1
    end
end


-- checking if the boss just got attacked
function boss:attacked()
    if player.attacking and self.withinAttackRangeBool then
        if self.first then
            boss.health = boss.health - 1
            self.hurtBool = true
            self.first = false
            love.audio.play(self.hit)
        end
    end
end

-- chages directions of the boss
function boss:changeDir()
    self.scaleX = - self.scaleX
    self.xVel = -self.xVel
    self.xVelTimer = 0
end

-- syncs the physics of the boss
function boss:syncPhysics()
    self.x, self.y = self.p.body:getPosition()
    self.p.body:setLinearVelocity(self.xVel * self.speedmod, 100)
    if self.xVelTimer > 2000 then
        self:changeDir()
    else
        self.xVelTimer = self.xVelTimer + 1
    end
end


-- sets the boss to the next frame
function boss:setNewFrame()
    local anim = self.state
    if anim.current < anim.total then
        anim.current = anim.current + 1
    else
        anim.current = 1
    end
    self.animation.draw = anim.img[anim.current]
end

-- checks to animate the player
function boss:animate(dt)
    self.animation.timer = self.animation.timer + dt
    if self.animation.timer > self.animation.rate then
        self.animation.timer = 0
        self:setNewFrame()
    end
end

-- gets each boss to update
function boss.update_all(dt)
    for i,instance in ipairs(activate_bosss) do
        instance:update(dt)
    end
end

-- handles collisions
function boss.beginContact(a, b, collision)
    for i,instance in ipairs(activate_bosss) do
        if a == instance.p.fixture or b == instance.p.fixture then
            if a == player.p.fixture or b == player.p.fixture then
                player:takeDamage(instance.damage)
                return true
            end
        end
    end
end

-- draws each boss
function boss:draw()
    local scaleX = 1
    if self.xVel < 0 then
        scaleX = -1
    end

    -- animates the hurt 
    if self.hurtBool then
        if self.turnRed then
            love.graphics.setColor(1, 0, 0) -- set color to red
        end
        self.turnRed = not self.turnRed
    end
    
    love.graphics.draw(self.animation.draw, self.x, self.y + self.offset_y, self.r, self.scaleX * 3, 3, self.w/9, self.h/6)
    
    -- love.graphics.polygon("line", self.p.body:getWorldPoints(self.p.shape:getPoints()))
    love.graphics.setColor(1, 1, 1)
end

-- gets each boss to be drawn
function boss.draw_all()
    for i,instance in ipairs(activate_bosss) do
        instance:draw()
    end
end

-- removes all the bosss
function boss:remove_all()
    for i,v in ipairs(activate_bosss) do
        v.p.body:destroy()
    end

    activate_bosss = {}
end


return boss
