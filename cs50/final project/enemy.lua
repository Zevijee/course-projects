local player = require 'player'

local enemy = {}
enemy.__index = enemy
local activate_enemys = {}

function enemy.new(x, y, damage, rage, scaleX, scaleY)    
    -- setting a new enemy instance
    local i = setmetatable({}, enemy)

    i.hit = love.audio.newSource('assets/sfx/hit.wav', 'static')

    i:loadAssets()

    i.damage = damage or 1

    -- dims and movement
    i.x = x
    i.y = y
    i.scaleX = 1
    i.offset_y = -8
    i.speedmod = 1
    i.speedmod = 1
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
    
    -- for the enemys health and if hurt
    i.currentHealth = 3
    i.hurtBool = false
    i.hurtCounter = 0
    i.turnRed = false
    i.first = true
    i.died = false
    i.withinAttackRangeBool = false
    
    table.insert(activate_enemys, i)

    if i.rage then
        i.state = i.animation.run
    else
        i.state = i.animation.walk
    end
end

function enemy:loadAssets()
    enemy.runAnim = {}
    for i=1, 4 do
        enemy.runAnim[i] = love.graphics.newImage('assets/gfx/enemy/run/' ..i.. '.png')
    end

    enemy.walkAnim = {}
    for i=1, 4 do
        enemy.walkAnim[i] = love.graphics.newImage('assets/gfx/enemy/walk/' ..i.. '.png')
    end

    enemy.w = enemy.walkAnim[1]:getWidth()
    enemy.h = enemy.walkAnim[1]:getHeight()
end

-- updates each enemy
function enemy:update(dt)
    self:syncPhysics()
    self:animate(dt)
    self:attacked()
    self:hurt()
    self:die()
    self:withinAttackRange()
end

-- checks if enemy is within the attack range of the player
function enemy:withinAttackRange()
    local distanceToPlayerX = math.abs(self.x - player.d.x)
    local distanceToPlayerY = math.abs(self.y - player.d.y)

    if distanceToPlayerX <= player.attackRange and distanceToPlayerY <= 16 then
        self.withinAttackRangeBool = true
    else
        self.withinAttackRangeBool = false
    end
end

-- kills the enemy
function enemy:kill()
    for i, instance in ipairs(activate_enemys) do
        if instance == self then
            self.p.body:destroy()
            table.remove(activate_enemys, i)
            player:increment_coins(5)
        end
    end
end

-- checks if the player died 
function enemy:die()
    if self.currentHealth <= 0 then
        self:kill()
    end
end

-- makes a enemy hurt anim
function enemy:hurt()
    if self.hurt and self.hurtCounter > 500 then
        self.hurtBool = false
        self.hurtCounter = 0
        self.first = true
    elseif self.hurt then
        self.hurtCounter  = self.hurtCounter + 1
    end
end


-- checking if the enemy just got attacked
function enemy:attacked()
    if player.attacking and self.withinAttackRangeBool then
        if self.first then
            self.currentHealth = self.currentHealth - 1
            self.hurtBool = true
            self.first = false
            love.audio.play(self.hit)
        end
    end
end

-- chages directions of the enemy
function enemy:changeDir()
    self.scaleX = - self.scaleX
    self.xVel = -self.xVel
    self.xVelTimer = 0
end

-- syncs the physics of the enemy
function enemy:syncPhysics()
    self.x, self.y = self.p.body:getPosition()
    self.p.body:setLinearVelocity(self.xVel * self.speedmod, 100)
    if self.xVelTimer > 1000 then
        self:changeDir()
    else
        self.xVelTimer = self.xVelTimer + 1
    end
end


-- sets the enemy to the next frame
function enemy:setNewFrame()
    local anim = self.state
    if anim.current < anim.total then
        anim.current = anim.current + 1
    else
        anim.current = 1
    end
    self.animation.draw = anim.img[anim.current]
end

-- checks to animate the player
function enemy:animate(dt)
    self.animation.timer = self.animation.timer + dt
    if self.animation.timer > self.animation.rate then
        self.animation.timer = 0
        self:setNewFrame()
    end
end

-- gets each enemy to update
function enemy.update_all(dt)
    for i,instance in ipairs(activate_enemys) do
        instance:update(dt)
    end
end

-- handles collisions
function enemy.beginContact(a, b, collision)
    for i,instance in ipairs(activate_enemys) do
        if a == instance.p.fixture or b == instance.p.fixture then
            if a == player.p.fixture or b == player.p.fixture then
                player:takeDamage(instance.damage)
                return true
            end
        end
    end
end

-- draws each enemy
function enemy:draw()
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
    
    love.graphics.draw(self.animation.draw, self.x, self.y + self.offset_y, self.r, self.scaleX, 1, self.w/2, self.h/2)

    -- love.graphics.polygon("line", self.p.body:getWorldPoints(self.p.shape:getPoints()))
    
    love.graphics.setColor(1, 1, 1)
end

-- gets each enemy to be drawn
function enemy.draw_all()
    for i,instance in ipairs(activate_enemys) do
        instance:draw()
    end
end

-- removes all the enemys
function enemy:remove_all()
    for i,v in ipairs(activate_enemys) do
        v.p.body:destroy()
    end

    activate_enemys = {}
end


return enemy
