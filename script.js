const products = [
  {id:1,name:"Textured Relaxed Shirt",brand:"Roadster",category:"Clothing",price:899,old:1499,discount:"40% OFF",tag:"BESTSELLER",image:"https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=700&q=85"},
  {id:2,name:"Everyday Classic Sneakers",brand:"Campus",category:"Footwear",price:1299,old:1999,discount:"35% OFF",tag:"TRENDING",image:"https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=700&q=85"},
  {id:3,name:"Minimal Gold-Tone Watch",brand:"DressBerry",category:"Accessories",price:1599,old:2499,discount:"36% OFF",tag:"NEW",image:"https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=700&q=85"},
  {id:4,name:"Daily Glow Skincare Set",brand:" skincare edit",category:"Beauty",price:699,old:999,discount:"30% OFF",tag:"JUST IN",image:"https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=700&q=85"},
  {id:5,name:"Structured Everyday Tote",brand:"Style Union",category:"Accessories",price:1199,old:1899,discount:"37% OFF",tag:"POPULAR",image:"https://images.unsplash.com/photo-1548036328-c9fa89d128fa?auto=format&fit=crop&w=700&q=85"},
  {id:6,name:"Soft Cotton Home Cushion",brand:"Home Centre",category:"Home",price:549,old:899,discount:"39% OFF",tag:"HOME EDIT",image:"https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=700&q=85"},
  {id:7,name:"Weekend Casual Jacket",brand:"Roadster",category:"Clothing",price:1899,old:2999,discount:"37% OFF",tag:"TRENDING",image:"https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=700&q=85"},
  {id:8,name:"Kids Everyday Backpack",brand:"ეტ",category:"Kids",price:799,old:1299,discount:"38% OFF",tag:"NEW",image:"https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=700&q=85"}
];
let activeCategory = "All";
let searchTerm = "";
let wishlist = [];
let bag = [];
const grid = document.getElementById("productGrid");
const toast = document.getElementById("toast");
let toastTimer;
function money(value){return "₹"+value.toLocaleString("en-IN")}
function showToast(message){toast.textContent=message;toast.classList.add("show");clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove("show"),2200)}
function renderProducts(){
  let list = products.filter(p => (activeCategory==="All" || p.category===activeCategory) && (p.name+" "+p.brand+" "+p.category).toLowerCase().includes(searchTerm));
  const sort = document.getElementById("sortSelect").value;
  if(sort==="low") list.sort((a,b)=>a.price-b.price);
  if(sort==="high") list.sort((a,b)=>b.price-a.price);
  if(!list.length){grid.innerHTML='<div class="empty-state">No matching products found. Try another search.</div>';return}
  grid.innerHTML=list.map(p=>`
    <article class="product-card">
      <div class="product-image"><img src="${p.image}" alt="${p.name}" loading="lazy" onerror="this.style.display='none';this.parentElement.style.background='#eee5e2'"><span class="product-tag">${p.tag}</span><button class="wish-btn ${wishlist.includes(p.id)?"selected":""}" data-wish="${p.id}" aria-label="Add ${p.name} to wishlist">${wishlist.includes(p.id)?"♥":"♡"}</button></div>
      <div class="product-info"><h3>${p.brand}</h3><p>${p.name}</p><span class="price">${money(p.price)}</span><span class="old-price">${money(p.old)}</span><span class="discount">${p.discount}</span><button class="add-btn" data-add="${p.id}">ADD TO BAG +</button></div>
    </article>`).join("");
}
function updateCounts(){document.getElementById("wishCount").textContent=wishlist.length;document.getElementById("bagCount").textContent=bag.length}
grid.addEventListener("click",e=>{
  const wish=e.target.closest("[data-wish]");
  const add=e.target.closest("[data-add]");
  if(wish){const id=Number(wish.dataset.wish);wishlist=wishlist.includes(id)?wishlist.filter(x=>x!==id):[...wishlist,id];updateCounts();renderProducts();showToast(wishlist.includes(id)?"Added to wishlist":"Removed from wishlist")}
  if(add){const product=products.find(p=>p.id===Number(add.dataset.add));bag.push(product.id);updateCounts();showToast(product.name+" added to your bag")}
});
document.querySelectorAll(".category-tile").forEach(button=>button.addEventListener("click",()=>{
  document.querySelectorAll(".category-tile").forEach(x=>x.classList.remove("active"));
  button.classList.add("active");activeCategory=button.dataset.category;renderProducts();
}));
document.getElementById("searchInput").addEventListener("input",e=>{searchTerm=e.target.value.trim().toLowerCase();renderProducts()});
document.getElementById("sortSelect").addEventListener("change",renderProducts);
document.getElementById("wishlistButton").addEventListener("click",()=>showToast("Your wishlist has "+wishlist.length+" item(s)"));
document.getElementById("bagButton").addEventListener("click",()=>{
  if(!bag.length){showToast("Your shopping bag is empty");return}
  const total=bag.reduce((sum,id)=>sum+products.find(p=>p.id===id).price,0);
  showToast(bag.length+" item(s) in bag · Total "+money(total));
});
document.getElementById("menuToggle").addEventListener("click",()=>document.getElementById("mainNav").classList.toggle("open"));
renderProducts();updateCounts();