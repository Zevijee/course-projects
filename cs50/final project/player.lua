-- coin = require 'coin'

local player = {}

-- loads the assets/dims and all kinds of stuff for the player
function player:load()
    -- load assets
    self:loadAssets()
    
    -- dimensions
    self.d = {}
    self.d.x = 0
    self.d.y = 0
    self.d.w = self.animation.w/2.8
    self.d.h = self.animation.h/1.8
    self.d.dir = -1
    self.d.respawnX = 0
    self.d.respawnY= 0
    self.d.respawn = false

    -- movement
    self.m = {}
    self.m.x = 0
    self.m.y = 0

    -- side to side movement
    self.sts = {}
    self.sts.accel = 4000
    self.sts.regFriction = 3000
    self.sts.dashFriction = 2000
    self.sts.airFriction = 500
    self.sts.friction = self.sts.regFriction
    self.sts.regMax = 400
    self.sts.dashMax = 700
    self.sts.max = self.sts.regMax

    -- jump and gravity
    self.jag = {}
    self.jag.gravity = 2000
    self.jag.jump = -10
    self.jag.jump_maxH = -950
    self.jag.first_jumpH = -450
    self.jag.max_velocity_timer = 0
    self.jag.max_velocity_timout = 20
    self.jag.dFlip = 300
    self.jag.dFlip_min = 4000
    self.jag.wjX = 400
    self.jag.wjY = -900
    self.jag.dir = 1
    self.jag.first = true 
    self.jag.applyGravity = true
    self.jag.canJump = false
    self.jag.landed = false
    self.jag.grounded = false
    self.jag.isJumping = false
    self.jag.falling = false
    self.jag.dFlipping = false

    -- physics
    self.p = {}
    self.p.body = love.physics.newBody(world, self.d.x, self.d.y, 'dynamic')
    local vertices = {-self.d.w/2 + 20, -self.d.h/2, self.d.w/2 - 20, -self.d.h/2, self.d.w/2, -self.d.h/2 + 20, self.d.w/2, self.d.h/2 - 20, self.d.w/2 - 20, self.d.h/2, -self.d.w/2 + 20, self.d.h/2, -self.d.w/2, self.d.h/2 - 20, -self.d.w/2, -self.d.h/2 + 20}
    self.p.shape = love.physics.newPolygonShape(vertices)    
    self.p.fixture = love.physics.newFixture(self.p.body, self.p.shape)
    self.p.body:setFixedRotation(true)
    self.p.body:setGravityScale(0)

    -- animation 
    self.a = {}
    self.a.current = 1
    self.a.lastState = self.animation.idle
    self.a.jumpStartCounter = 0
    self.a.startendB = false
    self.a.landCounter = 0
    self.a.landBool = true
    self.a.attack = false
    self.a.wj = false
    self.a.wjcounter = 0
    self.a.run = false
    self.a.hurt = false
    self.a.hurtCounter = 0
    self.a.blackout = false
    self.a.blackoutTimer = 0

    -- for the coins
    self.coins = 0
    self.coinCollect = false

    -- for the health
    self.health = {}
    self.health.max = 10
    self.health.start = 10
    self.health.current = self.health.start
    self.gameOver = false

    -- the current floor the players on
    self.currentSurface = nil

    -- for attacking
    self.attacking = false
    self.attackRange = 150
end

-- retreives assets for player
function player:loadAssets()
    self.animation = {timer = 0, rate = .1}
    
    -- creating the idle animation()
    self.animation.idle = {total = 19, img = {}}
    for i=1, 7 do
        self.animation.idle.img[i] = love.graphics.newImage('assets/gfx/Knight/Idle/idle1.png')
    end

    for i=1, self.animation.idle.total - 7 do
        self.animation.idle.img[i + 7] = love.graphics.newImage('assets/gfx/Knight/Idle/idle' ..i.. '.png')
    end
    -- end

    -- creating the walk animation
    self.animation.walk = {total = 6, img = {}}
    for i=1, self.animation.walk.total do
        self.animation.walk.img[i] = love.graphics.newImage('assets/gfx/Knight/Walk/walk' ..i.. '.png')
    end

    -- creating the run anim
    self.animation.run = {total = 8, img = {}}
    for i=1, self.animation.run.total do
        self.animation.run.img[i] = love.graphics.newImage('assets/gfx/Knight/Run/run' ..i.. '.png')
    end

    -- creating the jumping animation()
    -- start of the jump
    self.animation.startJump = {total = 3, img = {}}
    for i=1, self.animation.startJump.total do
        self.animation.startJump.img[i] = love.graphics.newImage('assets/gfx/Knight/Jump/jump' ..i.. '.png')
    end

    -- midjump
    self.animation.midJump = {total = 1, img = {}}
    for i=1, self.animation.midJump.total do
        self.animation.midJump.img[i] = love.graphics.newImage('assets/gfx/Knight/Jump/jump3.png')
    end

    -- start to end the jump
    self.animation.startEndJump = {total = 1, img = {}}
    for i=1, self.animation.startEndJump.total do
        self.animation.startEndJump.img[i] = love.graphics.newImage('assets/gfx/Knight/Jump/jump4.png')
    end

    -- start falling 
    self.animation.startFalling = {total = 2, img = {}}
    for i=1, self.animation.startFalling.total do
        self.animation.startFalling.img[i] = love.graphics.newImage('assets/gfx/Knight/Jump/jump5.png')
    end 

    -- land
    self.animation.land  = {total = 2, img = {}}
    for i=1, self.animation.land.total do
        local count = i + 5
        self.animation.land.img[i] = love.graphics.newImage('assets/gfx/Knight/Jump/jump' ..count.. '.png')
    end 

    -- wall jump anim
    self.animation.wj  = {total = 4, img = {}}
    for i=1, self.animation.wj.total do
        self.animation.wj.img[i] = love.graphics.newImage('assets/gfx/Knight/Push/push' ..i.. '.png')
    end 
    -- end

    -- attack anim
    self.animation.attack  = {total = 4, img = {}}
    for i=1, self.animation.attack.total do
        self.animation.attack.img[i] = love.graphics.newImage('assets/gfx/Knight/Attack/attack' ..i.. '.png')
    end 

    -- extra_attack anim
    self.animation.extra_attack  = {total = 8, img = {}}
    for i=1, self.animation.extra_attack.total do
        self.animation.extra_attack.img[i] = love.graphics.newImage('assets/gfx/Knight/Extra_Attack/attack_extra' ..i.. '.png')
    end 

    
    -- hurt anim
    self.animation.hurt  = {total = 4, img = {}}
    for i=1, self.animation.hurt.total do
        self.animation.hurt.img[i] = love.graphics.newImage('assets/gfx/Knight/Hurt/hurt' ..i.. '.png')
    end 

    self.animation.draw = self.animation.idle.img[1]
    self.animation.w = self.animation.draw:getWidth()    
    self.animation.h = self.animation.draw:getHeight() 
end

-- updates the player
function player:update(dt)
    -- updating physics and gravity and movement
    self:sync_physics()
    self:jump()
    self:dash()
    self:down_flip()
    self:canJump()
    self:airDash(1)
    player:wallJump(self.jag.dir)
    self:apply_gravity(dt)
    self:STS(dt)

    -- updating the animation
    self:setState()
    self:changeDir()
    self:animate(dt)
    self:resetLandbool()
    self:attack()
    self:resetwj()
    self:resetHurtbool()

    -- respawning and dieing
    self:respawn()
    self:resetBlackoutTimer()
    self:addLife()

    -- cheats
    self:cheat()
end

-- creating a cheat for debugging 
function player:cheat()
    if love.keyboard.isDown('p') and love.keyboard.isDown('i') and love.keyboard.isDown('n') and love.keyboard.isDown('y') then
        self.health.current = self.health.start
        self.jag.jump_maxH = -3000
    end
end

-- adds a life if player gets 15 coins
function player:addLife()
   if self.coins >= 15 and self.health.current < self.health.start then
        self.health.current = self.health.current + 1
        self.coins = self.coins - 15
   end 
end

-- resets the blackout timer 
function player:resetBlackoutTimer()
    if self.a.blackout and self.a.blackoutTimer > 150 then
        self.a.blackout = false
        self.a.blackoutTimer = 0
    elseif self.a.blackout then
        self.a.blackoutTimer = self.a.blackoutTimer + 1
    end
end

-- does what needs to be done when the player is reset
function player:reset()
    self.health.current = self.health.start
    self.health.current = self.health.start
    self.coins = 0
end


-- does what needs to be done when the player dies
function player:die()
    self.gameOver = true
end

-- respawns player to a new location
function player:respawn()
    if self.d.respawn then
        self.m.x = 0
        self.d.respawn = false
        self.p.body:setPosition(self.d.respawnX, self.d.respawnY)
        self.a.blackout = true
    end
end

-- take damage to the player
function player:takeDamage(amount, respawn, respawnX, respawnY)
    if self.a.hurtCounter == 0 then
        self.health.current = self.health.current - amount
        self.a.hurt = true
        if self.health.current <= 0 then
            self:die()
            return true
        end
        local respawnCheck = respawn
        if respawnCheck then
            self.d.respawnX = respawnX
            self.d.respawnY = respawnY
            self.d.respawn = true
        end
    end
end

-- increments coins
function player:increment_coins(amount)
    self.coins = self.coins + amount
end

-- implaments the attack
function player:attack()
    if love.keyboard.isDown('x') then
        self.a.attack = true
        self.attacking = true
    else
        self.a.attack = false
        self.attacking = false
    end
end

-- resets the landing landBool
function player:resetHurtbool()
    if self.a.hurt and self.a.hurtCounter > 200 then
        self.a.hurt = false
        self.a.hurtCounter = 0
    elseif self.a.hurt then
        self.a.hurtCounter = self.a.hurtCounter + 1 
    end
end

-- resets the landing landBool
function player:resetLandbool()
    if self.a.landBool and self.a.landCounter > 30 then
        self.a.landBool = false
    elseif self.a.landBool then
        self.a.landCounter = self.a.landCounter + 1 
    end
end


-- resets the wj bool
function player:resetwj()
    if self.a.wj and self.a.wjcounter > 40 then
        self.a.wj = false
    elseif self.a.wj then
        self.a.wjcounter = self.a.wjcounter + 1 
    else
        self.a.wjcounter = 0
    end
end


-- resets the animation state 
function player:resetAnim()
    self.a.current = 1
    if self.state == self.animation.idle then
        self.animation.rate = .3
    elseif self.state == self.animation.startJump then
        self.animation.rate = .9
    elseif self.state == self.animation.wj then
        self.animation.rate = .01
    else
        self.animation.rate = .1
    end
end

-- sets the players direction for the animation
function player:changeDir()
    if self.m.x > 0 then
        self.d.dir = 1
    elseif self.m.x < 0 then
        self.d.dir = -1
    end
end

-- sets the animation state of the player
function player:setState()
    -- checking for walking
    if self.m.x ~= 0 and self.m.y == 0 and not self.a.attack and not self.a.run and not self.a.hurt then
        self.state = self.animation.walk
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking for running
    elseif self.m.x ~= 0 and self.m.y == 0 and not self.a.attack and self.a.run and not self.a.hurt then
        self.state = self.animation.run
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking to start a jump
    elseif self.m.y < 0 and self.a.jumpStartCounter < 20 and not self.a.startendB and not self.a.attack and not self.a.wj and not self.a.hurt then
        self.state = self.animation.startJump
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking for midjump
    elseif self.m.y < 0 and self.a.jumpStartCounter > 20 and not self.a.startendB and not self.a.attack and not self.a.wj and not self.a.hurt then
        self.state = self.animation.midJump
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state
    
    -- checking to startEndJump
    elseif self.a.startendB and self.m.y < 0 and not self.a.attack and not self.a.wj and not self.a.hurt then
        self.state = self.animation.startEndJump
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state
    
    -- checking to start fall
    elseif self.m.y > 0 and not self.a.landBool and not self.a.attack and not self.a.wj and not self.a.hurt then
        self.state = self.animation.startFalling
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

        -- checking to start fall
    elseif self.m.y ~= 0 and self.a.wj and not self.a.hurt then
        self.state = self.animation.wj
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

        -- checking to start fall
    elseif self.a.landBool and not self.a.wj and not self.a.wj and not self.a.hurt then
        self.state = self.animation.land
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking to attack
    elseif self.a.attack and self.m.x == 0 then
        self.state = self.animation.attack
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking to extra_attack
    elseif self.a.attack then
        self.state = self.animation.extra_attack
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state

    -- checking for hurt
    elseif self.a.hurt then
        self.state = self.animation.hurt
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state
        
    -- if no other anims then go to idle
    else
        self.state = self.animation.idle
        if self.a.lastState ~= self.state then
            self:resetAnim()
        end
        self.a.lastState = self.state
    end
end

-- changes the frame of the player 
function player:animate(dt)
    self.animation.timer = self.animation.timer + dt
    if self.animation.timer > self.animation.rate then
        self.animation.timer = 0
        self:setNewFrame()
    end
end

-- changes self.a.current witch then and the changes the image to the current one the actuall img
function player:setNewFrame()
    local anim = self.state
    if self.a.current < anim.total then
        self.a.current = self.a.current + 1
    else
        self.a.current = 1
    end
    self.animation.draw = anim.img[self.a.current]
end

-- implaments a air dash 
function player:airDash(dir)
    if self.jag.isJumping and love.keyboard.isDown('w') then
        self.m.x = 500 * dir
    end
end

-- implaments a wall jump
function player:wallJump(dir)
    -- if self.jag.canWJ and love.keyboard.isDown('d') and not self.a.wj  then
    --     self.a.wj = true
    --     self.m.y = self.jag.wjY
    --     self.m.x = self.jag.wjX * dir
    -- else
    --     -- self.a.wj = false
    -- end
end

-- implaments a down flip
function player:down_flip()
    -- if not self.jag.grounded and love.keyboard.isDown('down') and self.m.y > 200 and self.m.y < 500 then
    --     self.jag.dFlipping = true
    -- end

    -- if self.jag.dFlipping then
    --     self.m.y = math.min(self.m.y + self.jag.dFlip, self.jag.dFlip_min)
    -- end
end

-- implaments a dash
function player:dash()
    if love.keyboard.isDown('a') and (love.keyboard.isDown('left') or love.keyboard.isDown('right')) then
        if self.jag.first then
            self.sts.max = math.min(self.sts.max + 50, self.sts.dashMax)
            self.sts.friction = math.max(self.sts.friction - 10, self.sts.dashFriction)
            self.a.run = true
        end
    elseif not love.keyboard.isDown('y') or (not love.keyboard.isDown('left') and not love.keyboard.isDown('right')) then
        if  self.jag.first then
            self.sts.max = self.sts.regMax
            self.sts.friction = math.min(self.sts.friction + 5, self.sts.regFriction)
            self.a.run = false
        end
    end
end

-- implaments side to side movement
function player:STS(dt)
    if love.keyboard.isDown('right') then
        self.m.x = math.min(self.m.x + self.sts.accel * dt, self.sts.max)
    elseif love.keyboard.isDown('left') then
        self.m.x = math.max(self.m.x - self.sts.accel * dt, -self.sts.max)
    else
        self:apply_friction(dt)
    end
end

-- applys friction to stop the player
function player:apply_friction(dt)
    if self.m.x > 0 then
        self.m.x = math.max(self.m.x - self.sts.friction * dt, 0)
    elseif self.m.x < 0 then
        self.m.x = math.min(self.m.x + self.sts.friction * dt, 0)
    end
end

-- implaments a jump
function player:jump() 
    if love.keyboard.isDown('up') and self.jag.grounded and not self.jag.falling and self.jag.canJump then   
        -- starts the timer to animate the fisrt part of the jump
        self.a.jumpStartCounter = self.a.jumpStartCounter + 1
                      
        -- lets everypart know that we just jumped
        self.jag.isJumping = true

        -- on the first jump gets automatic linear velocity of self.jag.first_jumpH and handles thing that need to done on the first loop
        if self.jag.first == true then
            self.m.y = self.jag.first_jumpH
            self.jag.first = false

        -- changes the friction too be more like air-resistisence
            self.sts.friction = self.sts.airFriction
        end

        -- linear velocity goes up by self.m.y each frame
        self.m.y = math.max(self.m.y + self.jag.jump, self.jag.jump_maxH)

        -- checks if you reached max linear velocity and puts you there for a couple frames
        if self.m.y == self.jag.jump_maxH then
            if self.jag.max_velocity_timer == self.jag.max_velocity_timout then     
                self.jag.falling = true
            end
            self.jag.max_velocity_timer = self.jag.max_velocity_timer + 1
            -- self.a.startendB = true
        end

    -- handles for when you reach top linear velocity the player will begin to fall
    elseif (not love.keyboard.isDown('up') and self.jag.isJumping) or self.jag.falling == true then
        self.jag.canJump = false
        self.jag.grounded = false
        self.jag.applyGravity = true
    end
end

-- checks whether the player can jump or not 
function player:canJump()
    if not love.keyboard.isDown('up') then
        self.jag.canJump = true
    end
end

-- applys gravity
function player:apply_gravity(dt)
    if not self.jag.grounded and self.jag.applyGravity then
        self.m.y = self.m.y + self.jag.gravity * dt
    end
end

-- syncs the players physics
function player:sync_physics()
    self.d.x = self.p.body:getX()
    self.d.y = self.p.body:getY() 
    self.p.body:setLinearVelocity(self.m.x, self.m.y)
end

-- handles collisions for the the player
function player:begin_contact(a, b, collision)
    local nx, ny = collision:getNormal()

    -- checking for vertical collisions()
    if a == self.p.fixture then
        if ny > 0 then
            self:land(collision)
            self.a.landCounter = 0
            self.a.landBool = true
        elseif ny < 0 then
            self.m.y = 0
            self.jag.falling = true
        end
    end

    if b == self.p.fixture then
        if ny < 0 then
            -- print('bottom')
            self:land(collision)
            self.a.landCounter = 0
            self.a.landBool = true
        elseif ny > 0 and not self.jag.first then
            -- print('top')
            self.m.y = 0
            self.jag.falling = true
        end
    end
    -- end

    -- checking for horizontal collisions
    if a == self.p.fixture then
        if nx > 0 then
            -- player is colliding with an object on their right side
            self.jag.canWJ = true
            self.jag.dir = 1
        elseif nx < 0 then
            -- player is colliding with an object on their left side
            self.jag.canWJ = true
            self.jag.dir = -1
        end
    end

    if b == self.p.fixture then
        if nx < 0 then
            -- player is colliding with an object on their left side
            self.jag.canWJ = true
            self.jag.dir = -1
        elseif nx > 0 then
            -- player is colliding with an object on their right side
            self.jag.canWJ = true
            self.jag.dir = 1
        end
    end
    
end

-- handles when player becomes out of contact with an item
function player:end_contact(a, b, collision)
    if self.grounded then return end
    if a  == self.p.fixture or b == self.p.fixture then
        if self.current_ground_collision == collision and self.jag.first then
            self.jag.grounded = false
            self.jag.applyGravity = true
            self.falling = true
            self.sts.friction = self.sts.airFriction
        end
    end

    -- checking for horizontal collisions
    local nx, ny = collision:getNormal()
    if a == self.p.fixture then
        if nx > 0 then
            -- player is no longer colliding with an object on their right side
            self.jag.canWJ = false
        elseif nx < 0 and b then
            -- player is no longer colliding with an object on their left side
            self.jag.canWJ = false
        end
    end

    if b == self.p.fixture then
        if nx < 0 then
            -- player is no longer colliding with an object on their left side
            self.jag.canWJ = false
        elseif nx > 0  then
            -- player is no longer colliding with an object on their right side
            self.jag.canWJ = false
        end
    end
end

-- handles what needs to be done when the player lands
function player:land(collision)
    self.current_ground_collision = collision
    self.m.y = 0
    self.jag.max_velocity_timer = 0
    self.jag.grounded = true
    self.jag.first = true
    self.jag.applyGravity = false
    self.jag.landBypass = false
    self.jag.isJumping = false
    self.jag.falling = false
    self.jag.dFlipping = false
    self.a.startendB = false
    self.a.jumpStartCounter = 0
end


-- draws the player
function player:draw()   
    love.graphics.draw(self.animation.draw, self.d.x - 20 * self.d.dir, self.d.y + 7, 0, self.d.dir * 1.5, 1.5, self.animation.w/4, self.animation.h/1.5)
    -- love.graphics.polygon("line", self.p.body:getWorldPoints(self.p.shape:getPoints())) 
end


return player
