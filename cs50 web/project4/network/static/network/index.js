document.addEventListener('DOMContentLoaded', function() {
    noMorePost = false
    nextPage = 1
    let page = 1

    document.querySelector('#edit-post').style.display = 'none'

    // for the next page
    document.querySelector('#next').addEventListener('click', function() {
        loadNextPage()
    })

    document.querySelector('#previous').addEventListener('click', function() {
        loadPreviousPage()
    })


    // resets the page so that the unwanted text isnt seen
    document.querySelector('#view-profile').style.display = 'none'
    document.querySelector('#following-header').style.display = 'none';

    // calls the load post on with the all the pages on the first on refreshes
    load_posts('all', page, 0)

    // checking if a a profile is clicked
    // this is for my profile meaning the user
    document.querySelector('#my-profile').addEventListener('click', function() {
        load_profile(this.dataset.profile);
    })

    // and this is for a random profile on a post
    document.querySelector('#view-posts').addEventListener('click', function(event) {
        const profileBtn = event.target.closest('.profile-button');
        const edit = event.target.closest('.edit');
        const like = event.target.closest('#likeBtn')
        if (profileBtn){
            load_profile(profileBtn.dataset.profile);
        }
        if (edit){
            editPost(edit.dataset.id)
        }
        if (like) {
            likePost(like.dataset.post)
        }
    })

    // for the edit form
    document.querySelector('#edit-form').addEventListener('submit', function(event) {
        event.preventDefault()

        const editedText = document.querySelector('#edit-post-text').value;
        const postId = document.querySelector('#postId').value;

        saveEdit(editedText, postId)
    })

    document.querySelector('#following').addEventListener('click', function() {following()})
})


function load_posts(content, page, profile) {
    globalContent = content;
    globalPage = page;
    globalProfile = profile;

    fetch(`load_posts/${content}/${page}/${profile}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        userId = data.user;
        const parentContainer = document.querySelector('#view-posts');
        const posts = data.posts;
        const isAuthenticated = data.is_authenticated;
        const anyMorePosts = data.any_more_posts;
        const isPreviousPage = data.any_previous_pages;

        if (!anyMorePosts) {
            document.querySelector('#next').style.display = 'none';
        } else {
            document.querySelector('#next').style.display = 'block';
        }

        if (!isPreviousPage) {
            document.querySelector('#previous').style.display = 'none';
        } else {
            document.querySelector('#previous').style.display = 'block';
        }


        parentContainer.innerHTML = '';

        posts.forEach(post => {
            element = document.createElement('div')

            element.className = 'post-div'

            const likedByUser = post.liked_by.includes(userId);

            // retrieving the data
            const poster = post.poster;
            const posterId = post.posterId;
            const postId = post.id;
            const fullPost = post.text;
            const likes = post.liked_by.length;
            const profileId = post.posterId;
            const timestamp = new Date(post.timestamp).toLocaleString();

            let edit = null

            if (userId == profileId) {
                 edit = `<a href="#" class="edit" data-id='${post.id}'>Edit<a><br>`
            } else{
                 edit = ''
            }


            if (isAuthenticated && content !== 'profile') {
                fullPoster = `<a class="profile-button" href="#" data-profile="${posterId}"><strong>${poster}</strong></a>`
            } else {
                fullPoster = `<strong style="font-size: 28px">${poster}</strong>`
            }

            if (likedByUser) {
                likeBtn = `<button class="btn btn-primary liked" id="likeBtn" data-post="${postId}">Unlike</button>`
            } else {
                likeBtn = `<button class="btn btn-primary unliked" id="likeBtn" data-post="${postId}">Like</button>`
            }

            element.innerHTML = `
                        ${fullPoster}<br>
                        ${edit}
                        ${fullPost}<br>
                        ${timestamp}<br>
                         <span class="hearts">&hearts;</span><span id=likeAmount data-post="${postId}">${likes}</span>
                         ${likeBtn}
            `
            const br = document.createElement('br')

            parentContainer.appendChild(element)
            parentContainer.appendChild(br)

        })

    })
}

function load_profile(profile) {
    document.querySelector('#following-header').style.display = 'none';
    document.querySelector('#full-create-post').style.display = 'none';
    document.querySelector('#view-posts').innerHTML = '';
    document.querySelector('#view-profile').style.display = 'block';

    load_posts('profile', 1, profile)

    fetch(`profile/${profile}`)
    .then(response => response.json())
    .then(data => {
        viewProfile = document.querySelector('#view-profile');

        // extracting the data
        const profileId = data.user_id;
        const username = data.username;
        const followers = data.followers;
        const following = data.following;
        let isFollowing = data.is_following;

        if (isFollowing) {
            followAction = 'Unfollow';
        } else {
            followAction = 'Follow';
        }

        document.querySelector('#username').innerHTML = username;
        document.querySelector('#followers').innerHTML = followers;
        document.querySelector('#following-amount').innerHTML = following;

        const userId = document.querySelector('#userId').innerHTML

        const followBtn = document.querySelector('#follow-btn');

        const edit = document

        if (userId == profileId){
            followBtn.style.display = 'none';
        } else {
            followBtn.innerHTML = followAction;

            if (!followBtn.hasAttribute('data-event-added')) {
                followBtn.addEventListener('click', function() {
                    followUnfollow(followAction, profile)

                    if (isFollowing) {
                        document.querySelector('#followers').innerHTML--;
                        followBtn.innerHTML = 'Follow';
                        isFollowing = false;
                    } else {
                        document.querySelector('#followers').innerHTML++;
                        followBtn.innerHTML = 'Unfollow';
                        isFollowing = true;
                    }
                })
            }
        };
    })
}

function followUnfollow(followAction, profile) {
    fetch(`profile/${profile}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(message => {
        console.log(message)
    })
}


function following() {
    document.querySelector('#full-create-post').style.display = 'none';
    document.querySelector('#view-posts').innerHTML = '';
    document.querySelector('#view-profile').style.display = 'none'

    document.querySelector('#following-header').style.display = 'block';

    load_posts('following', 1, 0)
}

function loadNextPage() {
    console.log(globalPage)
    load_posts(globalContent, globalPage + 1, globalProfile)
}

function loadPreviousPage() {
    console.log(globalPage)
    load_posts(globalContent, globalPage - 1, globalProfile)
}

function editPost(post){
    fetch(`edit_post/${post}`)
    .then(response => response.json())
    .then(data => {
        const permission = data.permission
        if (permission){
            document.querySelector('#view-profile').style.display = 'none'
            document.querySelector('#following-header').style.display = 'none';
            document.querySelector('#full-create-post').style.display = 'none';
            document.querySelector('#previous').style.display = 'none';
            document.querySelector('#next').style.display = 'none';
            document.querySelector('#view-posts').innerHTML = '';

            const post = data.post
            document.querySelector('#edit-poster').innerHTML = post.poster
            document.querySelector('#edit-post-text').value = post.text;
            document.querySelector('#edit-timestamp').innerHTML = new Date(post.timestamp).toLocaleString();
            document.querySelector('#edit-likes').innerHTML = post.likes

            const form = document.querySelector('#edit-post');
            form.style.display = 'block';
            const postInput = document.createElement('input');
            postInput.type = 'hidden';
            postInput.id = 'postId';
            postInput.value = post.id
            form.appendChild(postInput)

        } else {
            alert('You cant edit a post thats not yours')
        }
    })
}

function saveEdit(text, postId){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`edit_post/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            action: 'edit',
            text: text
        })
    })
    .then(response => response.json())
    .then(data => {
        const permission = data.permission

        if (permission) {
            document.querySelector('#edit-post').style.display = 'none';
            load_posts('all', 1, 0)
            document.querySelector('#full-create-post').style.display = 'block';
            alert('posted successfully updated')
        }else{
            alert('You cant edit a post thats not yours')
        }
    })
}

function likePost(postId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`edit_post/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            action: 'like'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const likeBtn = document.querySelector(`#likeBtn[data-post="${postId}"]`);
        const likeAmount = document.querySelector(`#likeAmount[data-post="${postId}"]`);

        const gotLiked = data.got_liked

        if (gotLiked) {
            likeBtn.textContent = 'Unlike'
            likeAmount.textContent = parseInt(likeAmount.textContent) + 1;
        } else {
            likeBtn.textContent = 'Like'
            likeAmount.textContent = parseInt(likeAmount.textContent) - 1;
        }
    })
}