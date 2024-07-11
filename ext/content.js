document.addEventListener('mouseout', function (event) {
  let tagName = event.target.tagName.toLowerCase();
  let className = event.target.className;
  let id = event.target.id;
  if (tagName === 'div' && className === 'style-scope ytd-video-preview') {
    console.log('onout');
    let popups = document.querySelectorAll('.video-info-popup');
    console.log(`popusp length: ${popups.length}`)
    popups.forEach((e) => e.remove());
  }
});

document.addEventListener('mouseover', function (event) {
  let tagName = event.target.tagName.toLowerCase();
  let className = event.target.className;
  let id = event.target.id;
  console.log(`${tagName}, ${className}, ${id}`);
  // console.log(event.target);
  // if (tagName === 'ytd-video-preview') {
  //   let videoThumbnail = event.target;
  // } else
  if (tagName === 'div' && className === 'style-scope ytd-video-preview') {
    console.log('onhover');
    let videoThumbnail = document.querySelector('#media-container-link');
    console.log(videoThumbnail);
    showPopup(videoThumbnail);
  }
});

function showPopup(thumbnail) {
  let videoId = thumbnail.href.split('v=')[1];
  let popup = document.createElement('div');
  let popupId = `video-info-popup-${videoId}`;
  popup.id = popupId;
  popup.className = 'video-info-popup';
  popup.innerHTML = `
    <div id="loading">Loading...</div>
    <div id="clickbait-rating"></div>
    <div id="video-summary"></div>
    <div id="comments-summary"></div>
  `;
  document.body.appendChild(popup);

  let rect = thumbnail.getBoundingClientRect();
  popup.style.top = `${rect.top + window.scrollY + rect.height}px`;
  popup.style.left = `${rect.left + window.scrollX}px`;

  fetchVideoInfo(videoId, popupId);
}

function fetchVideoInfo(videoId, popupId) {
  fetch(`https://507e6687-4236-4ae1-9220-c40483674512-00-9piah707l5p1.spock.replit.dev/video-info?videoId=${videoId}`)
    .then(response => response.json())
    .then(data => {
      let parent = document.getElementById(popupId);
      parent.querySelector('#loading').style.display = 'none';
      parent.querySelector('#clickbait-rating').innerText = `🥇 Clickbait Rating: ${data.clickbaitRating}`;
      parent.querySelector('#video-summary').innerText = `🥈 Video Summary: ${data.videoSummary}`;
      parent.querySelector('#comments-summary').innerText = `🥉 TL;DR of Comments: ${data.commentsSummary}`;
    })
    .catch(error => {
      console.error('Error fetching video info:', error);
    });
}

