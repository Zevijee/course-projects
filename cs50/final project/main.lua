love.graphics.setDefaultFilter('nearest', 'nearest')
local p = require 'player'
local coin = require 'coin'
local STI = require 'sti'
local gui = require 'gui'
local spikes = require 'spikes'
local map = require 'map'
local cam = require 'cam'
local enemy = require 'enemy'
local boss = require 'boss'
local button = require 'button'



function love.load()    
    world = love.physics.newWorld(0, 0)
    world:setCallbacks(begin_contact, end_contact)
    p:load()
    map:init()
    gui:load()
    coinCollect = false

    background = love.graphics.newImage('assets/gfx/download2.jpg')
    enemy.loadAssets()
end

function love.update(dt)
    coin.update_all()
    p:update(dt)
    world:update(dt)
    map:update()
    gui:update(dt)
    enemy.update_all(dt)
    boss.update_all(dt)
    -- print('x: ' ..p.d.x.. ' y:' ..p.d.y)
    if map.currentLevel > 0 and map.currentLevel < 3 then
        cam:cameraStuff()
    end

end

function begin_contact(a, b, collision)
    coin.beginContact(a, b, collision)
    spikes.beginContact(a, b, collision)

    if coinCollect then
        coinCollect = false
        return true
    end

    enemy.beginContact(a, b, collision)
    boss.beginContact(a, b, collision)
    p:begin_contact(a, b, collision)
end

function end_contact(a, b, collision)
    p:end_contact(a, b, collision)
end

function love.draw()
    if map.currentLevel > 0 and map.currentLevel < 3 then
        love.graphics.draw(background, 0, 0)
    end
    
    if map.currentLevel > 0 and map.currentLevel < 3 then
        cam:draw()
        gui:draw()
    else
        map:draw()
    end

    if p.a.blackout then
        love.graphics.clear(0, 0, 0) -- Clears the screen with black color
        -- draw your game objects here  
    end
end

