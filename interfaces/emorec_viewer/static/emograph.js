EDGE_WIDTH = 4
NODE_RADIUS = 10

COLORS = [
	"#FF5A5A",  // 기쁨, 설렘, 상쾌함
	"#FF0000",  // 신남, 즐거움, 열정적
	"#646EFF",  // 슬픔, 후회, 우울
	"#0000FF",  // 짜증, 화남, 불쾌
	"rgb(200,200,200)",	 // 복합 감정
	"rgb(200,200,200)",	 // 기타 감정
	"rgb(200,200,200)",	 // 평범하다
]

let c = document.getElementById("my_canvas")
let ctx = c.getContext("2d")

drawline = (x1, y1, x2, y2, width=5) => {

	if(x2 < x1) [x1, x2] = [x2, x1], [y1, y2] = [y2, y1]
	else if(Math.abs(x2-x1) < 1e-10 && y2 < y1) [x2, x1], [y1, y2] = [y2, y1]

	let theta = Math.atan((y1-y2)/(x2-x1))
	if(Math.abs(x2-x1) < 1e-10) theta = -Math.PI / 2
	let c = Math.cos(theta), s = Math.sin(theta)
	ctx.rotate(-theta)
	let dx = x2 - x1, dy = y2 - y1
	let x = c*x1-s*y1, y = s*x1+c*y1, l = Math.sqrt(dx*dx+dy*dy)
	ctx.fillRect(x, y-width/2, l, width)
	ctx.beginPath()
	ctx.arc(x, y, width/2, 0, Math.PI * 2)
	ctx.fill()
	ctx.beginPath()
	ctx.arc(x+l, y, width/2, 0, Math.PI * 2)
	ctx.fill()
	ctx.rotate(theta)
}

drawGraph = (ind, data) => {

	ctx.clearRect(0, 0, c.width, c.height);

	records = data[Object.keys(data)[ind]]

	let width = c.width, height = c.height
	let origin_x = 0, origin_y = 0;
	{
		ctx.beginPath()
		let original_width = ctx.lineWidth
		ctx.lineWidth = 3
		ctx.strokeStyle = "#74828F"
		let up = 100, 
			down = 800,
			left = 50;
			right = 1750;
		ctx.moveTo(left, up)
		ctx.lineTo(left, down)
		ctx.stroke()
		ctx.moveTo(left, (up+down)/2)
		ctx.lineTo(right, (up+down)/2)
		ctx.stroke()
		ctx.lineWidth = original_width

		origin_x = left, origin_y = (up+down)/2
	}

	{
		let dmin = records[0].date, dmax = records[0].date
		for(record of records){
			if(dmin > record.date) dmin = record.date
			if(dmax < record.date) dmax = record.date
		}
		
		let padding = 100
		curx = origin_x, cury = origin_y
		for(record of records){
			let d = record.date
			let ind = record.cont_i
			let nx = Math.floor(origin_x + padding + (d - dmin)/(dmax - dmin) * (width - origin_x - 2*padding))
			let ny = origin_y + [-100, -200, 100, 200, 0, 0, 0][ind]
			ctx.fillStyle = "gray"
			drawline(curx, cury, nx, ny, EDGE_WIDTH)
			//ctx.lineTo(nx, ny)
			//ctx.stroke()
			curx = nx, cury = ny;
		}

		for(record of records){
			ctx.beginPath()
			let d = record.date
			let ind = record.cont_i
			let padding = 100
			let nx = Math.floor(origin_x + padding + (d - dmin)/(dmax - dmin) * (width - origin_x - 2*padding))
			let ny = origin_y + [-100, -200, 100, 200, 0, 0, 0][ind]
			ctx.arc(nx, ny, NODE_RADIUS, 0, Math.PI * 2)
			ctx.fillStyle = COLORS[ind]
			ctx.fill()
		}
	}
	document.getElementById("person_name").innerHTML = Object.keys(data)[ind]
}

statistics = (ind, data) => {
	records = Object.values(data)[ind]
	cnt = [0, 0, 0, 0, 0, 0, 0]
	for(record of records){
		cnt[record.cont_i] += 1
	}
	//document.getElementById("statistics").innerHTML += cnt.map((d, i)=>{return '<span style="color:' + COLORS[i] + '">'+Math.floor(d/records.length*100) + '%</span>'}) +'<br>'
	document.getElementById("statistics").innerHTML = cnt.map((d, i)=>{return '<span style="color:' + COLORS[i] + '">'+Math.floor(d/records.length*100) + '%</span>'})
}

get_counts = (ind, data) => {
	records = Object.values(data)[ind]
	cnt = [0, 0, 0, 0, 0, 0, 0]
	for(record of records){
		cnt[record.cont_i] += 1
	}
    total = cnt.reduce((a,b)=>a+b);
    for(i in cnt){
        cnt[i] /= total;
    }
    return cnt
}


details = (ind, data) => {
	records = Object.values(data)[ind]
    result = ""
    prev_date = ""
    for(record of records){
        result += "<br>" + record.date_f + " " + record.cont + " " + record.detail + "<br>"
    }
    $("#details").html(result)
}

draw_bar_graph = (dom_id, data, ind, color) => {
	values = []
    for(let i in data){
        datum = {
            "i": i,
            "x": data[i],
            "t": 0
        };
        if(i == ind) datum.t = 1;
        values.push(datum)
    }

	json_data = {
	  "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
	  "width": 300,
	  "height": 300,
	  "data": {
		"values": values
	  },
	  "mark": "bar",
	  "encoding": {
		"x": {"field": "i", "type": "ordinal", "axis": {"ticks": false, "labels": true, "title": "", "labelAngle": 0}},
		"y": {"field": "x", "type": "quantitative", "axis": {"ticks": false, "labels": true, "format": "%", "title": "", "grid": true}},
		"color": {
		  "type": "ordinal",
		  "field": "t",
		  "scale": {
			"range": [
			  "rgb(200, 200, 200)", color
			]
		  },
          "legend": null
		}
	  }
	}
	vegaEmbed(dom_id, json_data).then((result)=>{
    })
}

emo_bar_graph = (ind, data) => {
    n = Object.keys(data).length
    colors = ["rgb(254,148,148)", "rgb(255,0,0)", "rgb(133,142,255)", "rgb(0,0,255)",
        "rgb(112,48,160)", "rgb(203,159,135)", "rgb(0,0,0)"]
    for(let iter=1;iter<=7;iter++){
        projected = []
        for(let i=0;i<n;i++){
            if(i != ind) projected.push([get_counts(i, data)[iter-1], -1]);
            else projected.push([get_counts(i, data)[iter-1], 1]);
        }
        projected.sort((a, b) => b[0]-a[0])
        let new_ind = 0;
        for(let i=0;i<n;i++){
            if(projected[i][1] == 1) new_ind = i;
        }
        draw_bar_graph("#vis" + iter, projected.map((x)=>x[0]), new_ind, colors[iter-1]);
    }
}

draw_pie_graph = (ind, data) => {
	let counts = get_counts(ind, data)
	values = []
	for(let i=0;i<counts.length;i++){
        values.push({"id": i, "field": counts[i]})
	}
    pie_json = {
		  "$schema": "https://vega.github.io/schema/vega/v4.json",
		  "width": 200,
		  "height": 200,
		  "autosize": "none",

		  "signals": [
			{
			  "name": "startAngle", "value": 0,
			  "bind": {"input": "range", "min": 0, "max": 6.29, "step": 0.01}
			},
			{
			  "name": "endAngle", "value": 6.29,
			  "bind": {"input": "range", "min": 0, "max": 6.29, "step": 0.01}
			},
			{
			  "name": "padAngle", "value": 0,
			  "bind": {"input": "range", "min": 0, "max": 0.1}
			},
			{
			  "name": "innerRadius", "value": 0,
			  "bind": {"input": "range", "min": 0, "max": 90, "step": 1}
			},
			{
			  "name": "cornerRadius", "value": 0,
			  "bind": {"input": "range", "min": 0, "max": 10, "step": 0.5}
			},
			{
			  "name": "sort", "value": false,
			  "bind": {"input": "checkbox"}
			}
		  ],

		  "data": [
			{
			  "name": "table",
			  "values": values,
			  "transform": [
				{
				  "type": "pie",
				  "field": "field",
				  "startAngle": {"signal": "startAngle"},
				  "endAngle": {"signal": "endAngle"},
				  "sort": {"signal": "sort"}
				}
			  ]
			}
		  ],

		  "scales": [
			{
			  "name": "color",
			  "type": "ordinal",
			  "range": ["rgb(254,148,148)", "rgb(255,0,0)", "rgb(133,142,255)", "rgb(0,0,255)","rgb(112,48,160)", "rgb(203,159,135)", "rgb(200,200,200)"]
			}
		  ],

		  "marks": [
			{
			  "type": "arc",
			  "from": {"data": "table"},
			  "encode": {
				"enter": {
				  "fill": {"scale": "color", "field": "id"},
				  "x": {"signal": "width / 2"},
				  "y": {"signal": "height / 2"}
				},
				"update": {
				  "startAngle": {"field": "startAngle"},
				  "endAngle": {"field": "endAngle"},
				  "padAngle": {"signal": "padAngle"},
				  "innerRadius": {"signal": "innerRadius"},
				  "outerRadius": {"signal": "width / 2"},
				  "cornerRadius": {"signal": "cornerRadius"}
				}
			  }
			}
		  ]
		}
	vegaEmbed("#pie", pie_json)
}



$(document).ready(() => {
    $.ajax({
        url: '/emorec_data',
        success: (data) => {
            let page_ind = 0
            drawGraph(page_ind, data)
            statistics(page_ind, data)
            details(page_ind, data)
            emo_bar_graph(page_ind, data)
			draw_pie_graph(page_ind, data)
            document.addEventListener('keydown', function(event) {
                let n = Object.keys(data).length
                if(event.keyCode == 37) {
                    page_ind = (page_ind - 1 + n) % n
                    drawGraph(page_ind, data)
                    statistics(page_ind, data)
                    details(page_ind, data)
                    emo_bar_graph(page_ind, data)
					draw_pie_graph(page_ind, data)
                }
                else if(event.keyCode == 39) {
                    page_ind = (page_ind + 1) % n
                    drawGraph(page_ind, data)
                    statistics(page_ind, data)
                    details(page_ind, data)
                    emo_bar_graph(page_ind, data)
					draw_pie_graph(page_ind, data)
                }
            });
            $("#prev").click(()=>{
                let n = Object.keys(data).length
                page_ind = (page_ind - 1 + n) % n
                drawGraph(page_ind, data)
                statistics(page_ind, data)
                details(page_ind, data)
                emo_bar_graph(page_ind, data)
				draw_pie_graph(page_ind, data)
            })
            $("#next").click(()=>{
                let n = Object.keys(data).length
                page_ind = (page_ind + 1) % n
                drawGraph(page_ind, data)
                statistics(page_ind, data)
                details(page_ind, data)
                emo_bar_graph(page_ind, data)
				draw_pie_graph(page_ind, data)
            });
        }
    })
});
