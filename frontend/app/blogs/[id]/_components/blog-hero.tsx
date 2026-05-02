type BlogHeroProps = {
  hero_image?: string
}

const BlogHero = ({ hero_image }: BlogHeroProps) => {
  if (!hero_image) return null

  return (
    <div className="w-full aspect-[16/9] overflow-hidden rounded-lg bg-muted mb-8">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={hero_image}
        alt=""
        className="w-full h-full object-cover"
      />
    </div>
  )
}

export default BlogHero
