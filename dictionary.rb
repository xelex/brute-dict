##
# A simple brute dictionary class
class Dictionary
  def initialize(opt = {})
    @filters = []
    @filters_negative = []
    @power_cache = []
    alphabet(opt[:abc])
    length(opt[:len])
  end

  ##
  # Set alphabet
  def alphabet(abc)
    @alphabet = abc.to_s.chars.sort.uniq
    return reset()
  end

  ##
  # Set word length
  def length(len)
    @length = len.to_i
    return reset()
  end

  ##
  # Resets iterator
  def reset
    @iterator = 0
    @total = nil

    if @alphabet && !@alphabet.empty? && @length.to_i > 0
      (@length + 1).times { |v|
        @power_cache[v] = @alphabet.count ** v
      }
    end

    return self
  end

  ##
  # Set positive filter (regexp)
  # Operator "next" will return sorted items only
  def match(regexp)
    @filters.push(regexp)
    return reset()
  end

  ##
  # Set filter (regexp)
  # Operator "next" will return sorted items only
  def nomatch(regexp)
    @filters_negative.push(regexp)
    return reset()
  end

  ##
  # Return number of variations.
  # @return total number of variations (filters are not in use)
  def total
    if @total_cache.nil?
      @total_cache = @alphabet.count ** @length
    end
    return @total_cache
  end

  ##
  # Return next part of variants (prioritized goes first)
  def next(n = 1)
    result = []

    while @iterator < total() && result.count < n
      word = n_to_word(@iterator)
      if check_filter(word)
        result.push(word)
      end
      @iterator += 1
    end

    return result
  end

  ##
  # Returns progress (in percents)
  def progress
    @iterator / total()
  end

  private
  def n_to_word(n)
    return '' if @alphabet.count == 0

    div = [0] * @length
    @length.times { |pow|
      div[pow] = (n % @power_cache[pow + 1])/ @power_cache[pow]
    }

    return div.map{|i| @alphabet[i]}.join()
  end

  def check_filter(word)
    return false if @filters.find{|filter| !filter.match(word)}
    return false if @filters_negative.find{|filter| filter.match(word)}

    return true
  end
end