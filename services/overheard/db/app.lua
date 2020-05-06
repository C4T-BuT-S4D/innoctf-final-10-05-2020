#!/usr/bin/env tarantool
-- Configure database

clock = require('clock')

box.cfg {
   listen = 3301
}
box.once("bootstrap", function()
   s=box.schema.space.create('users')
   s:create_index('primary', { type = 'TREE', parts = {{field = 1, type = 'string'}}})
   box.schema.sequence.create('postId', {min=1, start=1})
   s=box.schema.space.create('posts');
   s:create_index('primary', { type = 'TREE', sequence='postId', parts = {{field = 1, type = 'unsigned'}}})
   s:create_index('user', { type = 'TREE', unique=false, parts = {{field = 2, type = 'string'}}})
end)


function filterRecords(records, fn)
out = {}
for i, p in pairs(records) do if fn(p) then out[#out + 1] = p end end
return out
end

function addUser(login, password)
    u = box.tuple.new({login, password})
    return box.space.users:insert(u)[1]
end

function findUser(login, password)
    u = box.space.users:select(login)[1]
    if u == nil then return nil end
    if (password ~= nil) then if password == u[2] then return u[1] else return nil end else return u[1] end
    return nil
end

function addPost(user_id, text, is_draft)
    p = box.tuple.new({nil, user_id, text, is_draft, clock.time()})
    return box.space.posts:insert(p)[1]
end

function userPosts(user_id, paginator)
    return box.space.posts.index.user:select(user_id, paginator)
end

function latestPosts(paginator)
    paginator['iterator'] = 'REQ'
    posts = filterRecords(box.space.posts:select(paginator), function(p) return p[4] == false end)
    return posts
end

function findPost(post_id)
    return box.space.posts:select(post_id)[1]
end

function updatePost(post_id, user_id, text, is_draft)
    p = box.tuple.new({post_id, user_id, text, is_draft, clock.time()})
    return box.space.posts:replace(p)[0]
end








