
//adjust footer bottom
function ct() {
	return document.compatMode == "BackCompat" ? document.body.clientHeight : document.documentElement.clientHeight;
}
var f = document.getElementById('footer');
(window.onresize = function () {
		f.style.position = document.body.scrollHeight > ct() ? '' : 'absolute';
})();

// search event
	// click search btn
$('#searchBtn').click(function() {
	search()
});
	// press enter
$('#inputField').keydown(function(e){
	if (e.keyCode == 13) {
	 search()
	}
});

// go backend to search
function search() {
	var q = $('#inputField').val();
	if (q == "" || q == null || q == undefined) {
		location.href='/';
	} else {
		//parse special char
		var  entry = { "'": "&apos;", '"': '&quot;', '<': '&lt;', '>': '&gt;' };
		q = q.replace(/(['")-><&\\\/\.])/g, function ($0) { return entry[$0] || $0; });

		var string = '/query?q=' + q;
		location.href = string;
	};

}
