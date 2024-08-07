local camera = require 'camera'
local cam = camera()

local map = require 'map'
local p = require 'player'
local coin = require 'coin'
local spikes = require 'spikes'
local enemy = require 'enemy'
local boss = require 'boss'

local camStuff = {}

camStuff.Yoffset = 150

-- keeps camera in the game 
function camStuff:cameraStuff()
    if map.currentLevel == 2 then 
        self.Yoffset = 300
    end
    
    cam:lookAt(p.d.x + 200, p.d.y - self.Yoffset)
    
    local w = love.graphics.getWidth()
    local h = love.graphics.getHeight()

    if cam.x < w/2 then
        cam.x = w/2
    end

    if cam.y < h/2 then
        cam.y = h/2
    end

    local mapW = map.level.width * map.level.tilewidth
    local mapH = map.level.height * map.level.tilewidth

    if cam.x > (mapW - w/2) then
        cam.x = (mapW - w/2)
    end
    
    if cam.y > (mapH - h/2) then
        cam.y = (mapH - h/2)
    end
end

function camStuff:draw()
    cam:attach()
        enemy.draw_all()
        p:draw()
        map:draw()
        coin.draw_all()
        spikes.draw_all()
        boss.draw_all()
        -- love.graphics.draw(background, 0,0)
    cam:detach()
end

return camStuff