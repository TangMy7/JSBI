import {cloneDeep} from 'lodash'

export function rulesMenu(menu,dyMenu){
    let menuArr = [];
    //遍历前端路由 判断menu里面的每一项的meta.title 是否后端返回里面有这个信息
    let arr = cloneDeep(menu)
    console.log("待处理菜单",arr)
    arr.forEach(ele => {
        dyMenu.forEach(item =>{
            if(ele.meta.title == item.name) {
                //继续判断下级菜单
                if(item.children && item.children.length > 0) {
                    ele.children = rulesMenu(ele.children,item.children)
                }
                menuArr.push(ele) 
            }
        })
    });
    return  menuArr
}