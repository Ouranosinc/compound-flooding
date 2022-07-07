Kcop_card_S<-function(p,d){
  choose(d+p-1,d)-p
}
# Kcop_card_S<-Vectorize(Kcop_card_S, vectorize.args = "d")