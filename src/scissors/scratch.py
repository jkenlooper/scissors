import svgwrite

dwg = svgwrite.Drawing('scratch.svg', size=(500,500), profile='full')
dwg.set_desc(title="Scratch drawing", desc="Just testing")

#add the defs element
clip_down_center = dwg.defs.add(dwg.clipPath())
clip_down_center['id'] = 'clip_down_center'
right_path = clip_down_center.add(
        dwg.path('M 250 0 L 250 250 L 200 300 L 500 500 L 500 0')
        )
#right_path['clip-rule'] = 'evenodd'
#clip_down_center.add(dwg.line((250,0), (250,500)))
clip_down_center.add(dwg.circle((200,20), 150))

test_rect = dwg.defs.add(
        dwg.rect((50,50), (400,400), fill="blue", id="test_rect")
        )

#dwg.defs.add(clip_down_center)

#test_rect = dwg.rect((50,50), (100,100))
g = dwg.add(dwg.g())
inserted_test_rect = g.add(dwg.use(test_rect, insert=(0,0)))
inserted_test_rect['clip-path'] = 'url(#clip_down_center)'
#test_rect['clip-path'] = '#clip_down_center'
#dwg.add(test_rect)

dwg.save()
