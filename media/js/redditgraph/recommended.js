var RedditGraph = RedditGraph || {};

RedditGraph.loadUserLinks = function(link){
  var link_container = jQuery("#recommended_links");
  var url = link.attr("href");
  
  jQuery.ajax({
    url: url,
    type: 'get',
    beforeSend: function(){
      link_container.html("<img src='/media/img/animated_progress.gif' alt='Loading Links...' />");
    },
    success: function(response_json){
      if (response_json && response_json.links){
        link_container.html("");
        var links = response_json.links;
        if (links.length == 0){
          link_container.html("No links found.");
        }
        else{
          jQuery.each(links, function(index){
            var link_id = links[index];
            var link = ich.link_template({'link_id': link_id });
            link_container.append(link);
          });
        }
      }
    }
  });
  
};

RedditGraph.activateUserLinks = function(){
  jQuery("#reddit_users").on("click", "a", function(e){
    e.preventDefault();
    var link = jQuery(this);
    RedditGraph.loadUserLinks(link);
  });
};

RedditGraph.loadInfiniteScroll = function(){
  jQuery('#reddit_users').infinitescroll({
      debug: true,
      navSelector  : "div.pagination",            
                     // selector for the paged navigation (it will be hidden)
      nextSelector : "div.pagination a.next",    
                     // selector for the NEXT link (to page 2)
      itemSelector : "#reddit_users div.reddit_user"          
                     // selector for all items you'll retrieve
                     
    });
};

jQuery(document).ready(function(){
  RedditGraph.activateUserLinks();
  RedditGraph.loadInfiniteScroll();
});