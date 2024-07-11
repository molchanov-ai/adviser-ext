// document.addEventListener('mouseout', function (event) {
//   let tagName = event.target.tagName.toLowerCase();
//   let className = event.target.className;
//   let id = event.target.id;
//   if (!shadowed && tagName === 'div' && className === 'style-scope ytd-video-preview') {
//     console.log('onout');
//   }
// });

document.addEventListener('mouseover', function (event) {
  let tagName = event.target.tagName.toLowerCase();
  let className = event.target.className;
  let id = event.target.id;
  console.log(`${tagName}, ${className}, ${id}`);
  // console.log(event.target);
  // if (tagName === 'ytd-video-preview') {
  //   let videoThumbnail = event.target;
  // } else
  if (className == 'video-info-popup' || tagName == 'svg' || tagName == 'img' || className == 'style-scope tp-yt-app-drawer' || className == 'yt-simple-endpoint style-scope ytd-mini-guide-entry-renderer' || className == '' || tagName == 'rect' || className == 'ldBar') {
    return;
  }
  if (tagName === 'div' && className === 'style-scope ytd-video-preview') {
    let popup = document.querySelector('.video-info-popup');
    console.log(popup);
    if (popup != null) {
      return;
    }
    console.log('onhover');
    let videoThumbnail = document.querySelector('#media-container-link');
    console.log(videoThumbnail);
    showPopup(videoThumbnail);
  } else {
    // TODO: also check that popup is not enabled yet
    let popups = document.querySelectorAll('.video-info-popup');
    console.log(`popusp length: ${popups.length}, ${tagName}, ${className}, ${id}`)
    popups.forEach((e) => e.remove());
  }
});

function showPopup(thumbnail) {
  if (thumbnail.href.includes('v=')) {
    var videoId = thumbnail.href.split('v=')[1].split('&')[0];
  } else if (thumbnail.href.includes('shorts')) {
    var videoId = thumbnail.href.split('/').at(-1);
  } else {
    console.error('Incompatible state');
    return;
  }
  if (videoId.includes('&')) {
    videoId = videoId.split('&')[0];
  }
  // TODO: this popup must not be hoverable
  let popup = document.createElement('div');
  let popupId = `video-info-popup-${videoId}`;
  popup.id = popupId;
  popup.className = 'video-info-popup';
  popup.innerHTML = `
    <div id="loading"></div>
    <div id="clickbait-rating"></div>
    <div id="video-summary"></div>
    <div id="comments-summary"></div>
  `;
  document.body.appendChild(popup);
  // let bar = '<div class="ldBar" data-value="50" data-preset="bubble"></div>';
  // popup.innerHTML += bar;
  // let barNode = document.createElement('div');
  // barNode.className ='ldBar';
  // popup.appendChild()
  var bar1 = new ldBar(popup.querySelector('#loading'), {"preset": "bubble"});
  /* ldBar stored in the element */
  // var bar2 = document.getElementById(popup.id).ldBar;
  bar1.set(60);

  let rect = thumbnail.getBoundingClientRect();
  popup.style.top = `${rect.top + window.scrollY + rect.height}px`;
  popup.style.left = `${rect.left + window.scrollX}px`;
  // popup.style.width = '600px';

  fetchVideoInfo(videoId, popupId);
}

function fetchVideoInfo(videoId, popupId) {
  fetch(`https://507e6687-4236-4ae1-9220-c40483674512-00-9piah707l5p1.spock.replit.dev/video-info?videoId=${videoId}`)
    .then(response => response.json())
    .then(data => {
      let parent = document.getElementById(popupId);
      console.log(parent.ldBar);
      parent.querySelector('#loading').remove();
      parent.querySelector('#clickbait-rating').innerText = `🥇 Clickbait Rating: ${data.clickbaitRating}`;
      parent.querySelector('#video-summary').innerText = `🥈 Video Summary: ${data.videoSummary}`;
      parent.querySelector('#comments-summary').innerText = `🥉 TL;DR of Comments: ${data.commentsSummary}`;
    })
    .catch(error => {
      console.error('Error fetching video info:', error);
    });
}

