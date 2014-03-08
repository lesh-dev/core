set t_Co=256
syntax on
set hlsearch
set expandtab
set tabstop=4
retab
set shiftwidth=4
" do not put this file on machines without color terminal
source ~/.vim/scripts/xoria256.vim
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/

" <F2> Change encoding
set  wildmenu
set  wcm=<Tab>
menu Enc.cp1251     :e ++enc=cp1251<CR>
menu Enc.koi8-r     :e ++enc=koi8-r<CR>
menu Enc.cp866      :e ++enc=ibm866<CR>
menu Enc.utf8       :e ++enc=utf8<CR>
menu Enc.utf-8      :set encoding=utf8<CR>
menu Enc.ucs-2le    :e ++enc=ucs-2le<CR>
map  <F2> :emenu Enc.<Tab>
