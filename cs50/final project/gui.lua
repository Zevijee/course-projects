local player = require 'player'
local map = require 'map'
local boss = require 'boss'

local gui = {}

function gui:load()
    self.font = love.graphics.newFont('assets/bit.ttf', 36)
    
    -- coins
    self.coins = {}
    self.coins.img = love.graphics.newImage('assets/gfx/coin.png')
    self.coins.width = self.coins.img:getWidth()
    self.coins.height = self.coins.img:getHeight()
    self.coins.scale = 3
    self.coins.x = love.graphics.getWidth() - 200
    self.coins.y = 50    

    -- hearts 
    self.hearts = {}
    self.hearts.img = love.graphics.newImage('assets/gfx/heart.png')
    self.hearts.width = self.hearts.img:getWidth()
    self.hearts.height = self.hearts.img:getHeight()
    self.hearts.x = 0
    self.hearts.y = 50
    self.hearts.scale = 3
    self.hearts.spacing = self.hearts.width * self.hearts.scale + 30

    -- boss hearts
    self.displayBossHeartsBool = false

end

function gui:update(dt)
    self:toDisplaybosses()
end

function gui:draw()
    self:display_coins()
    self:display_coins_txt()
    self:display_hearts()
    self:displayBossHearts()
end

-- checks if should display bosses hearts 
function gui:toDisplaybosses()
    if map.currentLevel == 2 then
        self.displayBossHeartsBool = true
    end
end

-- displays hearts 
function gui:display_hearts()
    for i=1, player.health.current do
        local x = self.hearts.x + self.hearts.spacing * i
        love.graphics.setColor(0,0,0,0.5)
        love.graphics.draw(self.hearts.img, x + 2, self.hearts.y + 2, 0, self.hearts.scale, self.hearts.scale)
        love.graphics.setColor(1,1,1,1)
        love.graphics.draw(self.hearts.img, x, self.hearts.y, 0, self.hearts.scale, self.hearts.scale)
    end
end

-- displays bosses hearts
function gui:displayBossHearts()
    if self.displayBossHeartsBool then
        for i=1, boss.health do
            local x = self.hearts.x + self.hearts.spacing * i
            love.graphics.setColor(0,0,0,0.5)
            love.graphics.draw(self.hearts.img, x + 2, 720 - 48, 0, self.hearts.scale, self.hearts.scale)
            love.graphics.setColor(0,1,0,1)
            love.graphics.draw(self.hearts.img, x,  720 - 50, 0, self.hearts.scale, self.hearts.scale)
            love.graphics.setColor(1,1,1,1)
        end
    end
end

-- displays the players coins
function gui:display_coins()
    love.graphics.setColor(0,0,0,0.5)
    love.graphics.draw(self.coins.img, self.coins.x, self.coins.y, 0, self.coins.scale, self.coins.scale)
    love.graphics.setColor(1,1,1,1)
    love.graphics.draw(self.coins.img, self.coins.x, self.coins.y, 0, self.coins.scale, self.coins.scale)
end

-- dispalys the amount of coins the player has
function gui:display_coins_txt()
    love.graphics.setFont(self.font)
    local x = self.coins.x + self.coins.width * self.coins.scale
    local y = self.coins.y + self.coins.height / 2 * self.coins.scale - self.font:getHeight()/2
    love.graphics.setColor(0,0,0,0.5)
    love.graphics.print(' : ' ..player.coins, x + 2, y + 2)
    love.graphics.setColor(1,1,1,1)
    love.graphics.print(' : ' ..player.coins, x, y)
end

return gui
