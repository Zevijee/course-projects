local STI = require 'sti'

local coin = require 'coin'
local spikes = require 'spikes'
local enemy = require 'enemy'
local p = require 'player'
local boss = require 'boss'
local button = require 'button'

local map = {}


map.win = love.audio.newSource('assets/sfx/win.wav', 'static')
map.lose = love.audio.newSource('assets/sfx/gameOver.wav', 'static')

map.currentLevel = 0

map.bossCounter = 0
map.boss = false

map.string = 'full Knight'

-- chages the game state to play
local function start()
    map.currentLevel = 1
    map:init()
    p.d.respawn = true
    p.d.respawnX = 100
    p.d.respawnY = 1000
end


function map:init()
    if map.currentLevel == 1 then
        self.level = STI('map/map.lua', {'box2d'})
        self.backgroundAudio = love.audio.newSource('assets/sfx/background.mp3', 'static')
    elseif map.currentLevel == 2 then
        self.level = STI('map/map2.lua', {'box2d'})
        self.backgroundAudio = love.audio.newSource('assets/sfx/bossBackgroundAudio.mp3', 'static')  
    elseif map.currentLevel == 3 then
        map.startButton = button('play', start, nil, 240, 80)
        map.exitButton = button('exit', love.event.quit, nil, 240, 80)
    else
        map.startButton = button('play', start, nil, 240, 80)
        map.exitButton = button('exit', love.event.quit, nil, 240, 80)
    end

    if self.currentLevel > 0 and self.currentLevel < 3 then
        self.level:box2d_init(world)
        self:spawn_entitys()
    end
end

function map:update(dt)
    self:checkForBoss()
    if self.currentLevel > 0 and self.currentLevel < 3 then
        love.audio.play(self.backgroundAudio)
    else
        local x, y = love.mouse.getPosition()
        self.startButton:check_pressed(x, y, 16)
        self.exitButton:check_pressed(x, y, 16)
    end

    -- print(self.currentLevel)

    if self.currentLevel == 2 then
        if self.bossCounter > 200 and not self.boss then
            boss.new(320, 624, 2, true)
            self.boss = true
        else
            self.bossCounter = self.bossCounter + 1
        end
    end

    if boss.number == 1 then
        love.audio.stop()
        love.audio.play(self.win)
        self.currentLevel = 3
        self:init()
        boss.number = 0
        self.boss = false
        map:clean()
        map.string = 'You Win!'
    end

    if p.gameOver then
        love.audio.stop()
        love.audio.play(self.lose)
        p.gameOver = false
        self.currentLevel = 3
        self:init()
        map:clean()
        p:reset()
        map.string = 'game over'
    end
    -- print(self.currentLevel)
end

function map:next(next)
    self.currentLevel = next
    self:clean()
    self:init()
    p.d.respawn = true
    p.d.respawnX = 0
    p.d.respawnY = 0
end

function map:checkForBoss()
    if p.d.x > 6300 and p.d.y < 150 then
        love.audio.stop()
        self:next(2)
    end
end

function map:draw()
    if self.currentLevel > 0 and self.currentLevel < 3 then
        self.level:drawLayer(self.level.layers['solid'])
        self.level:drawLayer(self.level.layers['ground'])
    else
        love.graphics.setColor(0, 0, 1)
        love.graphics.printf(map.string, 0, 150, love.graphics.getWidth(), 'center')
        love.graphics.setColor(0, 0, 0)
        map.startButton:draw(love.graphics.getWidth()/2 - 120, love.graphics.getHeight()/2 + 25, 17, 10)
        map.exitButton:draw(love.graphics.getWidth()/2 - 120, love.graphics.getHeight()/2 + 150, 17, 10)
    end
end

function map:clean()
    self.level:box2d_removeLayer('solid')
    coin.remove_all()
    enemy.remove_all()
    spikes.remove_all()
    boss.remove_all()
end

function map:spawn_entitys()
    for i,v in ipairs(self.level.layers.entity.objects) do
        if v.class == 'spike1' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 100, 1300)
        elseif v.class == 'spike2' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 1950, 1300)
        elseif v.class == 'spike3' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 2750, 1300)
        elseif v.class == 'spike4' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 3400, 1300)
        elseif v.class == 'spike5' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 4200, 1300)
        elseif v.class == 'spike6' then
            spikes.new(v.x - v.width/2, v.y - v.height/2, 1, true, 5000, 1300)
        elseif v.class == 'coin' then
            coin.new(v.x, v.y)
        elseif v.class == 'enemy' then
            enemy.new(v.x, v.y, 1)
        elseif v.class == 'enemy2' then
            enemy.new(v.x, v.y, 2, true)
        end
    end
end

return map