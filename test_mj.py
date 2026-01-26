from mj.mj import MahjongDeck, MahjongTile, SuitType, HonorType

# 测试1：创建牌堆并检查初始牌数
deck = MahjongDeck()
print(f'初始牌数: {len(deck)}')

# 测试2：洗牌
deck.shuffle()
print('洗牌完成')

# 测试3：摸牌
tile1 = deck.draw()
print(f'摸牌1: {tile1.full_name}')
tile2 = deck.draw_from_front()
print(f'摸牌2: {tile2.full_name}')

# 测试4：检查剩余牌数
print(f'剩余牌数: {deck.remaining()}')

# 测试5：重置牌堆
deck.reset()
print(f'重置后牌数: {len(deck)}')

# 测试6：测试验证器
print('测试验证器...')
try:
    # 测试正常创建
    normal_tile = MahjongTile(number=5, suit=SuitType.WAN, honor=None, tile_type='suit')
    print(f'正常创建: {normal_tile.full_name}')
    
except Exception as e:
    print(f'验证失败: {e}')

print('测试完成')
